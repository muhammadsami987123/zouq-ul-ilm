"""
AI-related utility functions.
"""

import random
import time
from typing import List, Optional, Dict, Any
import google.generativeai as genai


def rotate_api_key(api_keys: List[str]) -> Optional[str]:
    """
    Rotate through available API keys.
    
    Args:
        api_keys: List of available API keys
        
    Returns:
        Randomly selected API key
    """
    if not api_keys:
        return None
    
    return random.choice(api_keys)


def validate_api_key(api_key: str) -> bool:
    """
    Validate API key by making a test request.
    
    Args:
        api_key: API key to validate
        
    Returns:
        True if API key is valid
    """
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Make a simple test request
        response = model.generate_content("Test")
        return response.text is not None
    except Exception:
        return False


def get_model_config(model_name: str, config_type: str = "content_generation") -> Dict[str, Any]:
    """
    Get configuration for AI model based on type.
    
    Args:
        model_name: Name of the AI model
        config_type: Type of configuration (topic_extraction, content_generation, summarization)
        
    Returns:
        Model configuration dictionary
    """
    base_configs = {
        "topic_extraction": {
            "temperature": 0.3,
            "top_k": 40,
            "top_p": 0.8,
            "max_output_tokens": 500
        },
        "content_generation": {
            "temperature": 0.4,
            "top_k": 50,
            "top_p": 0.9,
            "max_output_tokens": 800
        },
        "summarization": {
            "temperature": 0.2,
            "top_k": 30,
            "top_p": 0.7,
            "max_output_tokens": 400
        }
    }
    
    config = base_configs.get(config_type, base_configs["content_generation"]).copy()
    
    # Model-specific adjustments
    if "pro" in model_name.lower():
        config["temperature"] = min(config["temperature"] + 0.1, 1.0)
        config["max_output_tokens"] = min(config["max_output_tokens"] + 200, 4000)
    elif "flash" in model_name.lower():
        config["temperature"] = max(config["temperature"] - 0.1, 0.0)
    
    return config


def format_prompt(prompt_template: str, **kwargs) -> str:
    """
    Format prompt template with provided variables.
    
    Args:
        prompt_template: Prompt template string
        **kwargs: Variables to substitute in template
        
    Returns:
        Formatted prompt
    """
    try:
        return prompt_template.format(**kwargs)
    except KeyError as e:
        print(f"Missing variable in prompt template: {e}")
        return prompt_template


def create_generation_config(
    temperature: float = 0.4,
    top_k: int = 50,
    top_p: float = 0.9,
    max_output_tokens: int = 800
) -> Dict[str, Any]:
    """
    Create generation configuration for AI model.
    
    Args:
        temperature: Temperature for generation
        top_k: Top-k parameter
        top_p: Top-p parameter
        max_output_tokens: Maximum output tokens
        
    Returns:
        Generation configuration
    """
    return {
        "temperature": temperature,
        "top_k": top_k,
        "top_p": top_p,
        "max_output_tokens": max_output_tokens,
        "response_mime_type": "text/plain"
    }


def get_model_by_name(model_name: str):
    """
    Get AI model instance by name.
    
    Args:
        model_name: Name of the model
        
    Returns:
        GenerativeModel instance
    """
    try:
        return genai.GenerativeModel(model_name)
    except Exception as e:
        print(f"Error creating model {model_name}: {e}")
        return None


def make_api_call_with_retry(
    model,
    prompt: str,
    max_retries: int = 3,
    delay: float = 2.0
) -> Optional[str]:
    """
    Make API call with retry logic.
    
    Args:
        model: AI model instance
        prompt: Prompt to send
        max_retries: Maximum number of retries
        delay: Delay between retries
        
    Returns:
        Response text or None if failed
    """
    for attempt in range(max_retries):
        try:
            response = model.generate_content(prompt)
            if response.text:
                return response.text
        except Exception as e:
            print(f"API call attempt {attempt + 1} failed: {e}")
            if attempt < max_retries - 1:
                time.sleep(delay * (attempt + 1))  # Exponential backoff
    
    return None


def estimate_tokens(text: str) -> int:
    """
    Estimate number of tokens in text (rough approximation).
    
    Args:
        text: Text to estimate
        
    Returns:
        Estimated token count
    """
    if not text:
        return 0
    
    # Rough estimation: 1 token ≈ 4 characters for English text
    return len(text) // 4


def check_rate_limit(api_calls_made: int, rate_limit: int = 20) -> bool:
    """
    Check if rate limit has been reached.
    
    Args:
        api_calls_made: Number of API calls made
        rate_limit: Rate limit per minute
        
    Returns:
        True if rate limit reached
    """
    return api_calls_made >= rate_limit


def get_optimal_model_for_task(task_type: str, available_models: List[str]) -> str:
    """
    Get optimal model for specific task type.
    
    Args:
        task_type: Type of task (topic_extraction, content_generation, summarization)
        available_models: List of available models
        
    Returns:
        Optimal model name
    """
    model_preferences = {
        "topic_extraction": ["gemini-2.0-flash", "gemini-1.5-flash"],
        "content_generation": ["gemini-1.5-pro", "gemini-2.0-flash"],
        "summarization": ["gemini-1.5-flash", "gemini-2.0-flash"]
    }
    
    preferred_models = model_preferences.get(task_type, ["gemini-2.0-flash"])
    
    for model in preferred_models:
        if model in available_models:
            return model
    
    # Fallback to first available model
    return available_models[0] if available_models else "gemini-1.5-flash"


def create_chat_session(model, history: Optional[List] = None):
    """
    Create chat session with optional history.
    
    Args:
        model: AI model instance
        history: Optional chat history
        
    Returns:
        Chat session
    """
    try:
        return model.start_chat(history=history or [])
    except Exception as e:
        print(f"Error creating chat session: {e}")
        return None


def send_message_with_fallback(
    chat_session,
    message: str,
    fallback_models: Optional[List[str]] = None
) -> Optional[str]:
    """
    Send message with fallback to other models if needed.
    
    Args:
        chat_session: Chat session
        message: Message to send
        fallback_models: List of fallback models
        
    Returns:
        Response text or None
    """
    try:
        response = chat_session.send_message(message)
        return response.text if response.text else None
    except Exception as e:
        print(f"Error sending message: {e}")
        
        # Try fallback models if available
        if fallback_models:
            for model_name in fallback_models:
                try:
                    model = get_model_by_name(model_name)
                    if model:
                        response = model.generate_content(message)
                        return response.text if response.text else None
                except Exception:
                    continue
        
        return None


def validate_response_quality(response: str, min_length: int = 10) -> bool:
    """
    Validate AI response quality.
    
    Args:
        response: AI response text
        min_length: Minimum response length
        
    Returns:
        True if response is valid
    """
    if not response or not response.strip():
        return False
    
    if len(response.strip()) < min_length:
        return False
    
    # Check for common error patterns
    error_patterns = [
        "I can't", "I cannot", "I'm not able", "I am not able",
        "Error:", "Exception:", "Failed to", "Unable to"
    ]
    
    response_lower = response.lower()
    for pattern in error_patterns:
        if pattern in response_lower:
            return False
    
    return True


def extract_content_from_response(response: str) -> str:
    """
    Extract clean content from AI response.
    
    Args:
        response: Raw AI response
        
    Returns:
        Cleaned content
    """
    if not response:
        return ""
    
    # Remove common prefixes
    prefixes_to_remove = [
        "Here's", "Here is", "The following", "Below is", "Here are",
        "I'll", "I will", "Let me", "I can", "I'll provide"
    ]
    
    content = response.strip()
    
    for prefix in prefixes_to_remove:
        if content.startswith(prefix):
            content = content[len(prefix):].strip()
            if content.startswith(":"):
                content = content[1:].strip()
            break
    
    return content
