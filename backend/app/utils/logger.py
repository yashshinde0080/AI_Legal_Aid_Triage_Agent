"""
Logging Configuration
Centralized logging setup for the application.
"""

import logging
import sys
from typing import Optional

from app.config import settings


# Create logger
logger = logging.getLogger("legal_aid")


def setup_logger(
    level: Optional[str] = None,
    format_string: Optional[str] = None
) -> logging.Logger:
    """
    Set up application logger.
    
    Args:
        level: Log level (DEBUG, INFO, WARNING, ERROR)
        format_string: Custom format string
        
    Returns:
        Configured logger
    """
    # Determine log level
    if level is None:
        level = "DEBUG" if settings.debug else "INFO"
    
    numeric_level = getattr(logging, level.upper(), logging.INFO)
    
    # Set format
    if format_string is None:
        format_string = (
            "%(asctime)s | %(levelname)-8s | %(name)s:%(funcName)s:%(lineno)d | %(message)s"
        )
    
    # Create formatter
    formatter = logging.Formatter(format_string)
    
    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    console_handler.setLevel(numeric_level)
    
    # Configure logger
    logger.setLevel(numeric_level)
    logger.handlers.clear()
    logger.addHandler(console_handler)
    
    # Prevent propagation to root logger
    logger.propagate = False
    
    # Reduce noise from other libraries
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)
    logging.getLogger("supabase").setLevel(logging.WARNING)
    
    logger.info(f"Logger initialized with level: {level}")
    
    return logger


class LogContext:
    """Context manager for adding context to logs."""
    
    def __init__(self, **context):
        self.context = context
        self.old_factory = None
    
    def __enter__(self):
        self.old_factory = logging.getLogRecordFactory()
        context = self.context
        
        def factory(*args, **kwargs):
            record = self.old_factory(*args, **kwargs)
            for key, value in context.items():
                setattr(record, key, value)
            return record
        
        logging.setLogRecordFactory(factory)
        return self
    
    def __exit__(self, *args):
        logging.setLogRecordFactory(self.old_factory)