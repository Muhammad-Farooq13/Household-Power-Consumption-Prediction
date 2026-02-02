"""Logger utility for the project."""
import logging
import os


def setup_logger(name: str, log_level: int = logging.INFO) -> logging.Logger:
    """
    Set up a logger with the given name and log level.
    
    Args:
        name: Name of the logger
        log_level: Logging level (default: logging.INFO)
    
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(log_level)
    
    # Create logs directory if it doesn't exist
    os.makedirs("logs", exist_ok=True)
    
    # File handler
    fh = logging.FileHandler(f"logs/{name}.log")
    fh.setLevel(log_level)
    
    # Console handler
    ch = logging.StreamHandler()
    ch.setLevel(log_level)
    
    # Formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    
    logger.addHandler(fh)
    logger.addHandler(ch)
    
    return logger
