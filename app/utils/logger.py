import logging
import sys
from typing import Optional

def setup_logger(name: str, level: Optional[int] = None) -> logging.Logger:
    """
    Configure and return a logger with the given name and level.
    
    Args:
        name: The name of the logger
        level: The logging level (defaults to INFO if None)
        
    Returns:
        A configured logger instance
    """
    if level is None:
        level = logging.INFO
        
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    if not logger.handlers:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(level)
        
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        console_handler.setFormatter(formatter)
        
        logger.addHandler(console_handler)
    
    return logger

app_logger = setup_logger("devin_tokunou_api")

api_logger = setup_logger("devin_tokunou_api.api")
db_logger = setup_logger("devin_tokunou_api.db")
