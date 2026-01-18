import logging
import os
from typing import Optional


def setup_logging(log_level: Optional[str] = None) -> None:
    """Configure root logger with formatted output."""
    if log_level is None:
        log_level = os.getenv("LOG_LEVEL", "INFO").upper()
    
    logging.basicConfig(
        level=getattr(logging, log_level, logging.INFO),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def get_logger(name: Optional[str] = None) -> logging.Logger:
    """Get a logger instance with the given name."""
    if name is None:
        name = __name__
    
    return logging.getLogger(name)


# Initialize logging on import
setup_logging()



