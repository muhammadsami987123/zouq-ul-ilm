"""
Logging utilities for the PPT Generation system.
"""

import logging
import logging.config
import os
from datetime import datetime
from typing import Optional, Dict, Any
from pathlib import Path


def setup_logging(
    log_level: str = "INFO",
    log_file: Optional[str] = None,
    log_format: Optional[str] = None
) -> None:
    """
    Setup logging configuration for the application.
    
    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Path to log file (optional)
        log_format: Custom log format (optional)
    """
    if log_format is None:
        log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Create logs directory if it doesn't exist
    if log_file:
        log_dir = os.path.dirname(log_file)
        if log_dir:
            Path(log_dir).mkdir(parents=True, exist_ok=True)
    
    # Configure logging
    config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "standard": {
                "format": log_format
            },
            "detailed": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(module)s - %(funcName)s - %(message)s"
            }
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": log_level,
                "formatter": "standard",
                "stream": "ext://sys.stdout"
            }
        },
        "loggers": {
            "ppt_generator": {
                "level": log_level,
                "handlers": ["console"],
                "propagate": False
            }
        }
    }
    
    # Add file handler if log_file is specified
    if log_file:
        config["handlers"]["file"] = {
            "class": "logging.FileHandler",
            "level": "DEBUG",
            "formatter": "detailed",
            "filename": log_file,
            "mode": "a"
        }
        config["loggers"]["ppt_generator"]["handlers"].append("file")
    
    logging.config.dictConfig(config)


def get_logger(name: str = "ppt_generator") -> logging.Logger:
    """
    Get logger instance.
    
    Args:
        name: Logger name
        
    Returns:
        Logger instance
    """
    return logging.getLogger(name)


def log_processing_step(
    logger: logging.Logger,
    step: str,
    details: Optional[Dict[str, Any]] = None,
    level: str = "INFO"
) -> None:
    """
    Log a processing step with details.
    
    Args:
        logger: Logger instance
        step: Step description
        details: Additional details
        level: Log level
    """
    message = f"Processing step: {step}"
    
    if details:
        detail_str = ", ".join([f"{k}={v}" for k, v in details.items()])
        message += f" | Details: {detail_str}"
    
    log_level = getattr(logging, level.upper(), logging.INFO)
    logger.log(log_level, message)


def log_performance_metrics(
    logger: logging.Logger,
    operation: str,
    duration: float,
    additional_metrics: Optional[Dict[str, Any]] = None
) -> None:
    """
    Log performance metrics for an operation.
    
    Args:
        logger: Logger instance
        operation: Operation name
        duration: Duration in seconds
        additional_metrics: Additional metrics to log
    """
    message = f"Performance: {operation} completed in {duration:.2f}s"
    
    if additional_metrics:
        metrics_str = ", ".join([f"{k}={v}" for k, v in additional_metrics.items()])
        message += f" | Metrics: {metrics_str}"
    
    logger.info(message)


def log_error_with_context(
    logger: logging.Logger,
    error: Exception,
    context: Optional[Dict[str, Any]] = None
) -> None:
    """
    Log error with additional context.
    
    Args:
        logger: Logger instance
        error: Exception that occurred
        context: Additional context information
    """
    message = f"Error: {type(error).__name__}: {str(error)}"
    
    if context:
        context_str = ", ".join([f"{k}={v}" for k, v in context.items()])
        message += f" | Context: {context_str}"
    
    logger.error(message, exc_info=True)


def create_log_file_name(prefix: str = "ppt_generator") -> str:
    """
    Create a log file name with timestamp.
    
    Args:
        prefix: Log file prefix
        
    Returns:
        Log file name
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{prefix}_{timestamp}.log"


def log_api_usage(
    logger: logging.Logger,
    model_name: str,
    tokens_used: Optional[int] = None,
    response_time: Optional[float] = None
) -> None:
    """
    Log API usage information.
    
    Args:
        logger: Logger instance
        model_name: AI model name used
        tokens_used: Number of tokens used (if available)
        response_time: Response time in seconds (if available)
    """
    message = f"API Usage: Model={model_name}"
    
    if tokens_used:
        message += f", Tokens={tokens_used}"
    
    if response_time:
        message += f", ResponseTime={response_time:.2f}s"
    
    logger.info(message)


def log_file_operation(
    logger: logging.Logger,
    operation: str,
    file_path: str,
    success: bool,
    additional_info: Optional[Dict[str, Any]] = None
) -> None:
    """
    Log file operation results.
    
    Args:
        logger: Logger instance
        operation: Operation type (read, write, delete, etc.)
        file_path: Path to the file
        success: Whether operation was successful
        additional_info: Additional information
    """
    status = "SUCCESS" if success else "FAILED"
    message = f"File Operation: {operation} {status} | File: {file_path}"
    
    if additional_info:
        info_str = ", ".join([f"{k}={v}" for k, v in additional_info.items()])
        message += f" | Info: {info_str}"
    
    log_level = logging.INFO if success else logging.ERROR
    logger.log(log_level, message)


def log_quality_metrics(
    logger: logging.Logger,
    metrics: Dict[str, Any]
) -> None:
    """
    Log content quality metrics.
    
    Args:
        logger: Logger instance
        metrics: Quality metrics dictionary
    """
    message = "Quality Metrics: " + ", ".join([f"{k}={v}" for k, v in metrics.items()])
    logger.info(message)


def setup_rotating_logger(
    log_file: str,
    max_bytes: int = 10 * 1024 * 1024,  # 10MB
    backup_count: int = 5,
    log_level: str = "INFO"
) -> logging.Logger:
    """
    Setup rotating file logger.
    
    Args:
        log_file: Path to log file
        max_bytes: Maximum file size before rotation
        backup_count: Number of backup files to keep
        log_level: Logging level
        
    Returns:
        Logger instance
    """
    from logging.handlers import RotatingFileHandler
    
    # Create logs directory if it doesn't exist
    log_dir = os.path.dirname(log_file)
    if log_dir:
        Path(log_dir).mkdir(parents=True, exist_ok=True)
    
    # Create logger
    logger = logging.getLogger("ppt_generator_rotating")
    logger.setLevel(getattr(logging, log_level.upper()))
    
    # Create rotating file handler
    handler = RotatingFileHandler(
        log_file,
        maxBytes=max_bytes,
        backupCount=backup_count
    )
    
    # Create formatter
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)
    
    # Add handler to logger
    logger.addHandler(handler)
    
    return logger


def log_system_info(logger: logging.Logger) -> None:
    """
    Log system information.
    
    Args:
        logger: Logger instance
    """
    import platform
    import sys
    
    system_info = {
        "Platform": platform.platform(),
        "Python Version": sys.version,
        "Architecture": platform.architecture()[0],
        "Processor": platform.processor()
    }
    
    message = "System Info: " + ", ".join([f"{k}={v}" for k, v in system_info.items()])
    logger.info(message)
