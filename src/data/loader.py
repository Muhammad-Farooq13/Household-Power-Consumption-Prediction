"""Data loading utilities."""
import pandas as pd
from pathlib import Path
from typing import Tuple
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


def load_raw_data(filepath: str) -> pd.DataFrame:
    """
    Load raw household power consumption data.
    
    Args:
        filepath: Path to the raw data file
    
    Returns:
        Loaded dataframe
    """
    logger.info(f"Loading data from {filepath}")
    try:
        df = pd.read_csv(
            filepath,
            sep=';',
            na_values='?',
            parse_dates={'datetime': ['Date', 'Time']},
            infer_datetime_format=True,
            low_memory=False
        )
        logger.info(f"Data loaded successfully. Shape: {df.shape}")
        return df
    except Exception as e:
        logger.error(f"Error loading data: {str(e)}")
        raise


def save_processed_data(df: pd.DataFrame, filepath: str) -> None:
    """
    Save processed data to a CSV file.
    
    Args:
        df: Dataframe to save
        filepath: Output path
    """
    logger.info(f"Saving processed data to {filepath}")
    try:
        df.to_csv(filepath, index=False)
        logger.info(f"Data saved successfully")
    except Exception as e:
        logger.error(f"Error saving data: {str(e)}")
        raise


def load_processed_data(filepath: str) -> pd.DataFrame:
    """
    Load processed data from a CSV file.
    
    Args:
        filepath: Path to processed data file
    
    Returns:
        Loaded dataframe
    """
    logger.info(f"Loading processed data from {filepath}")
    try:
        df = pd.read_csv(filepath)
        logger.info(f"Processed data loaded. Shape: {df.shape}")
        return df
    except Exception as e:
        logger.error(f"Error loading processed data: {str(e)}")
        raise
