"""
Logging configuration for browser orchestrator.
"""

import sys
from pathlib import Path
from loguru import logger
import yaml


def setup_logging(config_path: str = "config/app-config.yaml"):
    """Initialize logging with configuration."""
    
    # Load config if exists
    config_file = Path(config_path)
    if config_file.exists():
        with open(config_file) as f:
            config = yaml.safe_load(f)
            log_config = config.get("logging", {})
            level = log_config.get("level", "INFO")
            log_format = log_config.get("format")
            log_file = log_config.get("file")
    else:
        level = "INFO"
        log_format = None
        log_file = None
    
    # Remove default handler
    logger.remove()
    
    # Console output
    logger.add(
        sys.stdout,
        level=level,
        format=log_format or "{time:HH:mm:ss} | {level} | {message}",
        colorize=True
    )
    
    # File output
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        logger.add(
            log_file,
            level=level,
            format=log_format or "{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} - {message}",
            rotation="100 MB",
            retention="7 days",
            compression="zip"
        )
    
    return logger


def get_logger(name: str = "browser-orchestrator"):
    """Get a logger instance."""
    return logger.bind(name=name)
