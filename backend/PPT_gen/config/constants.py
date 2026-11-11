"""
Application constants and configuration values.
"""

from typing import Dict, List, Any

# AI Model Configuration
AI_MODELS = {
    "primary": "gemini-2.0-flash",
    "secondary": "gemini-1.5-flash",
    "advanced": "gemini-1.5-pro",
    "experimental": "gemini-2.0-flash-exp"
}

# Model rotation for content variety
MODEL_ROTATION = [
    "gemini-2.0-flash",
    "gemini-1.5-flash", 
    "gemini-1.5-pro",
    "gemini-2.0-flash"
]

# Template Categories
TEMPLATE_CATEGORIES = {
    "modern": ["Polyhedron", "gradation_green"],
    "professional": ["blue", "silver_stone"],
    "academic": ["green", "yellow_subhan"],
    "creative": ["Polyhedron", "gradation_green"]
}

# Content Quality Thresholds
CONTENT_QUALITY_THRESHOLDS = {
    "min_bullet_length": 50,
    "max_bullet_length": 200,
    "min_word_count": 8,
    "max_bullets_per_slide": 5,
    "similarity_threshold": 0.7,
    "min_topic_length": 5
}

# Processing Limits
PROCESSING_LIMITS = {
    "max_pages_per_document": 50,
    "max_topics_per_page": 20,
    "max_slides_per_presentation": 50,
    "rate_limit_delay": 2.0,
    "max_retries": 3
}

# Subject Area Detection Patterns
SUBJECT_PATTERNS = {
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

# Generation Configuration Templates
GENERATION_CONFIGS = {
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

# File Extensions
SUPPORTED_INPUT_FORMATS = [".pdf", ".docx", ".txt"]
SUPPORTED_OUTPUT_FORMATS = [".pptx", ".pdf", ".html"]

# Error Messages
ERROR_MESSAGES = {
    "file_not_found": "File not found: {file_path}",
    "api_key_missing": "No valid API key found. Please configure your Google AI Studio API key.",
    "pdf_processing_error": "Error processing PDF: {error}",
    "template_not_found": "Template not found: {template_name}",
    "content_generation_failed": "Failed to generate content for topic: {topic}",
    "invalid_file_format": "Unsupported file format: {format}. Supported formats: {supported}"
}

# Success Messages
SUCCESS_MESSAGES = {
    "processing_complete": "✅ Processing completed successfully!",
    "presentation_saved": "📊 Presentation saved as: {filename}",
    "topics_found": "📚 Found {count} unique topics",
    "slides_generated": "📄 Generated {count} slides",
    "template_loaded": "🎨 Template loaded: {template_name}"
}

# Logging Configuration
LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        },
        "detailed": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(module)s - %(funcName)s - %(message)s"
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "INFO",
            "formatter": "standard",
            "stream": "ext://sys.stdout"
        },
        "file": {
            "class": "logging.FileHandler",
            "level": "DEBUG",
            "formatter": "detailed",
            "filename": "logs/ppt_generator.log",
            "mode": "a"
        }
    },
    "loggers": {
        "ppt_generator": {
            "level": "DEBUG",
            "handlers": ["console", "file"],
            "propagate": False
        }
    }
}
