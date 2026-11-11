"""
AI service for handling Google Gemini API interactions.
"""

import time
import random
from typing import List, Optional, Dict, Any
import google.generativeai as genai

from ..config import get_settings, AI_MODELS, GENERATION_CONFIGS
from ..models import Topic, ProcessingConfig
from ..utils import (
    rotate_api_key,
    validate_api_key,
    get_model_config,
    make_api_call_with_retry,
    validate_response_quality,
    extract_content_from_response
)


class AIService:
    """Service for AI operations using Google Gemini."""
    
    def __init__(self):
        self.settings = get_settings()
        self.api_keys = self.settings.get_api_keys()
        self.current_api_key = None
        self.api_calls_made = 0
        self.last_api_call_time = 0
        
        # Initialize with a random API key
        if self.api_keys:
            self.current_api_key = rotate_api_key(self.api_keys)
            genai.configure(api_key=self.current_api_key)
    
    def _rotate_api_key(self) -> bool:
        """Rotate to next available API key."""
        if not self.api_keys:
            return False
        
        self.current_api_key = rotate_api_key(self.api_keys)
        genai.configure(api_key=self.current_api_key)
        return True
    
    def _check_rate_limit(self) -> bool:
        """Check if we need to wait due to rate limiting."""
        current_time = time.time()
        time_since_last_call = current_time - self.last_api_call_time
        
        if time_since_last_call < self.settings.rate_limit_delay:
            sleep_time = self.settings.rate_limit_delay - time_since_last_call
            time.sleep(sleep_time)
        
        return True
    
    def _make_api_call(self, model_name: str, prompt: str, config_type: str = "content_generation") -> Optional[str]:
        """Make API call with proper error handling and rate limiting."""
        try:
            # Check rate limit
            self._check_rate_limit()
            
            # Get model configuration
            config = get_model_config(model_name, config_type)
            
            # Create model
            model = genai.GenerativeModel(model_name, generation_config=config)
            
            # Make API call with retry
            response = make_api_call_with_retry(
                model,
                prompt,
                max_retries=self.settings.max_retries,
                delay=self.settings.rate_limit_delay
            )
            
            # Update counters
            self.api_calls_made += 1
            self.last_api_call_time = time.time()
            
            # Validate response quality
            if response and validate_response_quality(response):
                return extract_content_from_response(response)
            
            return None
            
        except Exception as e:
            print(f"API call failed: {e}")
            # Try rotating API key
            if self._rotate_api_key():
                return self._make_api_call(model_name, prompt, config_type)
            return None
    
    def extract_topics(self, text: str, model_name: str = None) -> List[Topic]:
        """
        Extract topics from text using AI.
        
        Args:
            text: Text to extract topics from
            model_name: AI model to use (optional)
            
        Returns:
            List of extracted topics
        """
        if not text or not text.strip():
            return []
        
        if not model_name:
            model_name = AI_MODELS["primary"]
        
        # Create topic extraction prompt
        prompt = f"""
        Analyze the following academic content and extract the main topics/concepts covered.

        Content: {text}

        Instructions:
        - Identify the core topics, concepts, theories, or subjects mentioned
        - Make each topic clear and specific (3-10 words)
        - Focus on educational concepts that can be explained in a presentation
        - Include both main topics and important subtopics
        - Avoid administrative details, page numbers, references
        - Don't include generic words like "introduction", "overview", "summary"
        - Each topic should be suitable as a slide title
        - List one topic per line
        - No bullet points, numbers, or special formatting
        """
        
        response = self._make_api_call(model_name, prompt, "topic_extraction")
        
        if not response:
            return []
        
        # Parse response into topics
        topics = []
        for line in response.splitlines():
            line = line.strip()
            if line and len(line) > 3:
                topic = Topic(
                    text=line,
                    confidence=1.0,
                    category=None
                )
                topics.append(topic)
        
        return topics
    
    def generate_slide_content(self, topic: str, subject_context: str = "", model_name: str = None) -> List[str]:
        """
        Generate slide content for a topic.
        
        Args:
            topic: Topic to generate content for
            subject_context: Subject area context
            model_name: AI model to use (optional)
            
        Returns:
            List of bullet points for the slide
        """
        if not topic or not topic.strip():
            return []
        
        if not model_name:
            model_name = AI_MODELS["primary"]
        
        # Create content generation prompt
        prompt = f"""
        Create detailed slide content for the topic: "{topic}"
        {f"Subject context: {subject_context}" if subject_context else ""}

        Generate 5-8 comprehensive bullet points that thoroughly explain this topic.

        Requirements for each bullet point:
        - 15-35 words per point (detailed explanations, not single lines)
        - Use clear, educational language appropriate for students
        - Include specific examples, definitions, or details where relevant
        - Cover different aspects of the topic (definition, importance, examples, applications)
        - Make each point informative and educational
        - Use complete sentences that provide real value
        - Include technical terms with brief explanations when needed
        - Ensure points build understanding progressively

        Format: Write each point as a complete sentence, one per line, no bullets or numbers.

        Example for "Photosynthesis Process":
        Photosynthesis is the biological process where plants convert sunlight carbon dioxide and water into glucose and oxygen
        The process occurs primarily in chloroplasts which contain chlorophyll pigments that capture light energy effectively
        Light dependent reactions take place in thylakoids where water molecules are split to release oxygen as a byproduct
        Calvin cycle occurs in the stroma where carbon dioxide is fixed into organic molecules using ATP and NADPH
        Plants produce glucose through photosynthesis which serves as their primary energy source for growth and metabolism
        This process is essential for life on Earth as it produces the oxygen that most organisms need for respiration
        Factors affecting photosynthesis rate include light intensity temperature carbon dioxide concentration and water availability
        """
        
        response = self._make_api_call(model_name, prompt, "content_generation")
        
        if not response:
            return []
        
        # Parse response into bullet points
        bullets = []
        for line in response.splitlines():
            line = line.strip()
            if line and len(line) > 20:  # Minimum length for meaningful content
                bullets.append(line)
        
        return bullets
    
    def detect_subject_area(self, topics: List[str]) -> str:
        """
        Detect subject area from topics.
        
        Args:
            topics: List of topic texts
            
        Returns:
            Detected subject area
        """
        if not topics:
            return "General Academic"
        
        # Combine first few topics for analysis
        combined_text = " ".join(topics[:5]).lower()
        
        # Subject area detection patterns
        subject_patterns = {
            "Computer Science": [
                "network", "algorithm", "programming", "database", "software", 
                "computer", "data structure", "coding", "python", "java", "c++"
            ],
            "Biology": [
                "cell", "organism", "dna", "protein", "evolution", "photosynthesis", 
                "genetics", "anatomy", "physiology", "ecosystem"
            ],
            "Chemistry": [
                "molecule", "atom", "reaction", "compound", "element", "bond", 
                "acid", "base", "organic", "inorganic"
            ],
            "Physics": [
                "force", "energy", "wave", "particle", "quantum", "motion", 
                "electricity", "magnetism", "thermodynamics", "mechanics"
            ],
            "Mathematics": [
                "equation", "theorem", "calculus", "algebra", "geometry", 
                "probability", "statistics", "trigonometry", "linear algebra"
            ],
            "History": [
                "war", "empire", "revolution", "century", "ancient", "medieval", 
                "dynasty", "civilization", "culture", "politics"
            ],
            "Economics": [
                "market", "economy", "trade", "finance", "money", "supply", 
                "demand", "economic", "business", "investment"
            ],
            "Psychology": [
                "behavior", "cognitive", "mental", "brain", "psychology", 
                "social", "personality", "development", "therapy"
            ]
        }
        
        for subject, keywords in subject_patterns.items():
            if any(keyword in combined_text for keyword in keywords):
                return subject
        
        return "General Academic"
    
    def get_available_models(self) -> List[str]:
        """Get list of available AI models."""
        return list(AI_MODELS.values())
    
    def get_model_for_task(self, task_type: str) -> str:
        """Get optimal model for specific task type."""
        model_preferences = {
            "topic_extraction": ["gemini-2.0-flash", "gemini-1.5-flash"],
            "content_generation": ["gemini-1.5-pro", "gemini-2.0-flash"],
            "summarization": ["gemini-1.5-flash", "gemini-2.0-flash"]
        }
        
        preferred_models = model_preferences.get(task_type, ["gemini-2.0-flash"])
        available_models = self.get_available_models()
        
        for model in preferred_models:
            if model in available_models:
                return model
        
        return available_models[0] if available_models else "gemini-1.5-flash"
    
    def get_api_usage_stats(self) -> Dict[str, Any]:
        """Get API usage statistics."""
        return {
            "api_calls_made": self.api_calls_made,
            "current_api_key": self.current_api_key[:10] + "..." if self.current_api_key else None,
            "available_keys": len(self.api_keys),
            "last_call_time": self.last_api_call_time
        }
    
    def reset_api_usage(self) -> None:
        """Reset API usage counters."""
        self.api_calls_made = 0
        self.last_api_call_time = 0
