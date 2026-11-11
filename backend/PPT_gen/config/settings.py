"""
Application settings and configuration management.
"""

import os
from typing import Optional, List
from pydantic import BaseSettings, Field
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    """Application settings with environment variable support."""
    
    # API Configuration
    google_api_key: Optional[str] = Field(default=None, env="GOOGLE_API_KEY")
    api_key_1: Optional[str] = Field(default=None, env="API_KEY_1")
    api_key_2: Optional[str] = Field(default=None, env="API_KEY_2")
    api_key_3: Optional[str] = Field(default=None, env="API_KEY_3")
    
    # Processing Configuration
    max_pages_per_document: int = Field(default=50, env="MAX_PAGES_PER_DOCUMENT")
    rate_limit_delay: float = Field(default=2.0, env="RATE_LIMIT_DELAY")
    max_retries: int = Field(default=3, env="MAX_RETRIES")
    
    # Content Generation
    default_temperature: float = Field(default=0.4, env="DEFAULT_TEMPERATURE")
    default_top_k: int = Field(default=50, env="DEFAULT_TOP_K")
    default_top_p: float = Field(default=0.9, env="DEFAULT_TOP_P")
    max_output_tokens: int = Field(default=800, env="MAX_OUTPUT_TOKENS")
    
    # Quality Thresholds
    min_bullet_length: int = Field(default=50, env="MIN_BULLET_LENGTH")
    max_bullet_length: int = Field(default=200, env="MAX_BULLET_LENGTH")
    min_word_count: int = Field(default=8, env="MIN_WORD_COUNT")
    similarity_threshold: float = Field(default=0.7, env="SIMILARITY_THRESHOLD")
    
    # File Paths
    templates_dir: str = Field(default="templates", env="TEMPLATES_DIR")
    output_dir: str = Field(default="output", env="OUTPUT_DIR")
    logs_dir: str = Field(default="logs", env="LOGS_DIR")
    temp_dir: str = Field(default="temp", env="TEMP_DIR")
    
    # Logging
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    log_format: str = Field(
        default="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        env="LOG_FORMAT"
    )
    
    # Development
    debug_mode: bool = Field(default=False, env="DEBUG_MODE")
    enable_caching: bool = Field(default=True, env="ENABLE_CACHING")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
    
    def get_api_keys(self) -> List[str]:
        """Get list of available API keys."""
        keys = []
        for key in [self.google_api_key, self.api_key_1, self.api_key_2, self.api_key_3]:
            if key:
                keys.append(key)
        return keys
    
    def get_random_api_key(self) -> Optional[str]:
        """Get a random API key from available keys."""
        import random
        keys = self.get_api_keys()
        return random.choice(keys) if keys else None


# Global settings instance
_settings: Optional[Settings] = None


def get_settings() -> Settings:
    """Get global settings instance."""
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings


def reload_settings() -> Settings:
    """Reload settings from environment."""
    global _settings
    _settings = Settings()
    return _settings
