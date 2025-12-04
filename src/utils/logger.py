"""
Logging utility for SAVVI application.

Provides structured logging with console and file output, log rotation, and
configurable log levels for development and production environments.
"""

import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler
from typing import Optional
from datetime import datetime

from src.utils.config import get_config


def get_logger(name: str, log_level: Optional[str] = None) -> logging.Logger:
    """
    Get a logger instance for the specified module.
    
    Args:
        name: Logger name (typically __name__ of the calling module)
        log_level: Optional log level override (DEBUG, INFO, WARNING, ERROR, CRITICAL)
                   If None, uses level from configuration
    
    Returns:
        Configured Logger instance
    """
    logger = logging.getLogger(name)
    
    # Avoid adding handlers multiple times if logger already configured
    if logger.handlers:
        return logger
    
    # Get configuration (with fallback if config not available)
    try:
        from src.utils.config import get_config
        config = get_config()
        logging_settings = config.get_logging_settings()
    except Exception:
        # Fallback if config not available (e.g., during bootstrap)
        logging_settings = {
            "level": "INFO",
            "debug": False,
            "log_dir": "logs"
        }
    
    # Determine log level
    if log_level is None:
        log_level = logging_settings.get("level", "INFO")
    
    # Convert string level to logging constant
    numeric_level = getattr(logging, log_level.upper(), logging.INFO)
    logger.setLevel(numeric_level)
    
    # Create formatters
    detailed_formatter = logging.Formatter(
        fmt='%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    simple_formatter = logging.Formatter(
        fmt='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%H:%M:%S'
    )
    
    # Console handler (always add)
    console_handler = logging.StreamHandler(sys.stdout)
    if logging_settings.get("debug", False):
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(detailed_formatter)
    else:
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(simple_formatter)
    logger.addHandler(console_handler)
    
    # File handler with rotation
    log_dir = Path(logging_settings.get("log_dir", "logs"))
    log_dir.mkdir(parents=True, exist_ok=True)
    
    log_file = log_dir / f"savvi_{datetime.now().strftime('%Y%m%d')}.log"
    
    # Rotating file handler: 10MB per file, keep 5 backup files
    file_handler = RotatingFileHandler(
        filename=str(log_file),
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=5,
        encoding='utf-8'
    )
    file_handler.setLevel(logging.DEBUG)  # File always gets all levels
    file_handler.setFormatter(detailed_formatter)
    logger.addHandler(file_handler)
    
    # Prevent propagation to root logger
    logger.propagate = False
    
    return logger


def setup_root_logger(log_level: Optional[str] = None) -> None:
    """
    Configure the root logger for the application.
    
    This should be called once at application startup.
    
    Args:
        log_level: Optional log level override
    """
    try:
        from src.utils.config import get_config
        config = get_config()
        logging_settings = config.get_logging_settings()
    except Exception:
        # Fallback if config not available
        logging_settings = {
            "level": "INFO",
            "debug": False,
            "log_dir": "logs"
        }
    
    if log_level is None:
        log_level = logging_settings.get("level", "INFO")
    
    numeric_level = getattr(logging, log_level.upper(), logging.INFO)
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(numeric_level)
    
    # Remove existing handlers to avoid duplicates
    root_logger.handlers.clear()
    
    # Create formatter
    formatter = logging.Formatter(
        fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(numeric_level)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)
    
    # File handler
    log_dir = Path(logging_settings.get("log_dir", "logs"))
    log_dir.mkdir(parents=True, exist_ok=True)
    
    log_file = log_dir / f"savvi_{datetime.now().strftime('%Y%m%d')}.log"
    
    file_handler = RotatingFileHandler(
        filename=str(log_file),
        maxBytes=10 * 1024 * 1024,
        backupCount=5,
        encoding='utf-8'
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    root_logger.addHandler(file_handler)


# Default logger instance for convenience
logger = get_logger(__name__)

