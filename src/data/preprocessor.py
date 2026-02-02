"""Data preprocessing utilities."""
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from typing import Tuple, Optional
from src.utils.logger import setup_logger
from src.utils.config import (
    MISSING_VALUE_THRESHOLD, OUTLIER_STD_DEV, FEATURE_SCALING, RANDOM_STATE
)

logger = setup_logger(__name__)


class DataPreprocessor:
    """Handles data preprocessing operations."""
    
    def __init__(self, scaler_type: str = FEATURE_SCALING):
        """
        Initialize preprocessor.
        
        Args:
            scaler_type: Type of scaler ('standard' or 'minmax')
        """
        self.scaler = StandardScaler() if scaler_type == 'standard' else MinMaxScaler()
        self.numeric_columns = []
        
    def handle_missing_values(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Handle missing values in the dataframe.
        
        Args:
            df: Input dataframe
        
        Returns:
            Dataframe with missing values handled
        """
        logger.info("Handling missing values")
        
        # Drop columns with too many missing values
        missing_ratio = df.isnull().sum() / len(df)
        cols_to_drop = missing_ratio[missing_ratio > MISSING_VALUE_THRESHOLD].index
        
        if len(cols_to_drop) > 0:
            logger.info(f"Dropping columns with > {MISSING_VALUE_THRESHOLD*100}% missing: {cols_to_drop.tolist()}")
            df = df.drop(columns=cols_to_drop)
        
        # Fill remaining missing values with forward fill then backward fill
        df = df.fillna(method='ffill').fillna(method='bfill')
        
        logger.info("Missing values handled")
        return df
    
    def remove_outliers(self, df: pd.DataFrame, columns: Optional[list] = None) -> pd.DataFrame:
        """
        Remove outliers using standard deviation method.
        
        Args:
            df: Input dataframe
            columns: Columns to check for outliers. If None, check all numeric columns
        
        Returns:
            Dataframe with outliers removed
        """
        logger.info("Removing outliers")
        
        if columns is None:
            columns = df.select_dtypes(include=[np.number]).columns
        
        for col in columns:
            mean = df[col].mean()
            std = df[col].std()
            lower_bound = mean - (OUTLIER_STD_DEV * std)
            upper_bound = mean + (OUTLIER_STD_DEV * std)
            
            initial_len = len(df)
            df = df[(df[col] >= lower_bound) & (df[col] <= upper_bound)]
            removed = initial_len - len(df)
            
            if removed > 0:
                logger.info(f"Removed {removed} outliers from {col}")
        
        return df
    
    def scale_features(self, df: pd.DataFrame, columns: Optional[list] = None, fit: bool = True) -> pd.DataFrame:
        """
        Scale numeric features.
        
        Args:
            df: Input dataframe
            columns: Columns to scale. If None, scale all numeric columns
            fit: Whether to fit the scaler on this data
        
        Returns:
            Dataframe with scaled features
        """
        logger.info(f"Scaling features with {self.scaler.__class__.__name__}")
        
        if columns is None:
            columns = df.select_dtypes(include=[np.number]).columns
        
        self.numeric_columns = columns.tolist()
        
        if fit:
            df[columns] = self.scaler.fit_transform(df[columns])
        else:
            df[columns] = self.scaler.transform(df[columns])
        
        return df
    
    def preprocess(self, df: pd.DataFrame, fit: bool = True) -> pd.DataFrame:
        """
        Apply full preprocessing pipeline.
        
        Args:
            df: Input dataframe
            fit: Whether to fit scalers on this data
        
        Returns:
            Preprocessed dataframe
        """
        logger.info("Starting full preprocessing pipeline")
        
        df = self.handle_missing_values(df)
        df = self.remove_outliers(df)
        df = self.scale_features(df, fit=fit)
        
        logger.info("Preprocessing complete")
        return df
