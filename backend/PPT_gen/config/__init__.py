"""
Configuration module for PPT Generation system.
Contains all settings, constants, and configuration management.
"""

from .settings import Settings, get_settings
from .constants import (
    AI_MODELS,
    TEMPLATE_CATEGORIES,
    CONTENT_QUALITY_THRESHOLDS,
    PROCESSING_LIMITS
)

__all__ = [
    'Settings',
    'get_settings',
    'AI_MODELS',
    'TEMPLATE_CATEGORIES',
    'CONTENT_QUALITY_THRESHOLDS',
    'PROCESSING_LIMITS'
]
