"""Feature engineering utilities."""
import pandas as pd
import numpy as np
from datetime import datetime
from typing import List
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


class FeatureEngineer:
    """Handles feature engineering operations."""
    
    def __init__(self):
        """Initialize feature engineer."""
        self.engineered_features = []
    
    def extract_temporal_features(self, df: pd.DataFrame, datetime_col: str = 'datetime') -> pd.DataFrame:
        """
        Extract temporal features from datetime column.
        
        Args:
            df: Input dataframe
            datetime_col: Name of datetime column
        
        Returns:
            Dataframe with temporal features
        """
        logger.info("Extracting temporal features")
        
        df[datetime_col] = pd.to_datetime(df[datetime_col])
        
        df['hour'] = df[datetime_col].dt.hour
        df['day'] = df[datetime_col].dt.day
        df['month'] = df[datetime_col].dt.month
        df['year'] = df[datetime_col].dt.year
        df['day_of_week'] = df[datetime_col].dt.dayofweek
        df['quarter'] = df[datetime_col].dt.quarter
        df['is_weekend'] = (df['day_of_week'] >= 5).astype(int)
        
        self.engineered_features.extend(['hour', 'day', 'month', 'year', 'day_of_week', 'quarter', 'is_weekend'])
        
        logger.info(f"Temporal features extracted: {self.engineered_features}")
        return df
    
    def create_rolling_features(self, df: pd.DataFrame, feature_col: str, windows: List[int] = [24, 168]) -> pd.DataFrame:
        """
        Create rolling window features.
        
        Args:
            df: Input dataframe
            feature_col: Column to create rolling features for
            windows: List of window sizes (in hours)
        
        Returns:
            Dataframe with rolling features
        """
        logger.info(f"Creating rolling features for {feature_col}")
        
        for window in windows:
            df[f'{feature_col}_rolling_mean_{window}'] = df[feature_col].rolling(window=window).mean()
            df[f'{feature_col}_rolling_std_{window}'] = df[feature_col].rolling(window=window).std()
            self.engineered_features.extend([f'{feature_col}_rolling_mean_{window}', f'{feature_col}_rolling_std_{window}'])
        
        return df
    
    def create_lag_features(self, df: pd.DataFrame, feature_col: str, lags: List[int] = [1, 24, 168]) -> pd.DataFrame:
        """
        Create lagged features.
        
        Args:
            df: Input dataframe
            feature_col: Column to create lag features for
            lags: List of lag values
        
        Returns:
            Dataframe with lag features
        """
        logger.info(f"Creating lag features for {feature_col}")
        
        for lag in lags:
            df[f'{feature_col}_lag_{lag}'] = df[feature_col].shift(lag)
            self.engineered_features.append(f'{feature_col}_lag_{lag}')
        
        return df
    
    def engineer_features(self, df: pd.DataFrame, target_col: str = 'Global_active_power') -> pd.DataFrame:
        """
        Apply full feature engineering pipeline.
        
        Args:
            df: Input dataframe
            target_col: Name of target column
        
        Returns:
            Dataframe with engineered features
        """
        logger.info("Starting feature engineering pipeline")
        
        df = self.extract_temporal_features(df)
        df = self.create_rolling_features(df, target_col, windows=[24, 168])
        df = self.create_lag_features(df, target_col, lags=[1, 24, 168])
        
        # Drop NaN values created by rolling and lag operations
        df = df.dropna()
        
        logger.info(f"Feature engineering complete. Total engineered features: {len(self.engineered_features)}")
        return df
