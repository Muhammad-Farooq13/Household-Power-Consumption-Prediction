"""Tests for data loading and preprocessing."""
import pytest
import pandas as pd
import numpy as np
from pathlib import Path
from src.data.preprocessor import DataPreprocessor


@pytest.fixture
def sample_dataframe():
    """Create a sample dataframe for testing."""
    np.random.seed(42)
    return pd.DataFrame({
        'Global_active_power': np.random.randn(100) * 10 + 5,
        'Sub_metering_1': np.random.randn(100) * 5 + 2,
        'Sub_metering_2': np.random.randn(100) * 5 + 2,
        'Voltage': np.random.randn(100) * 10 + 240
    })


@pytest.fixture
def dataframe_with_missing():
    """Create a dataframe with missing values."""
    np.random.seed(42)
    df = pd.DataFrame({
        'Global_active_power': np.random.randn(100) * 10 + 5,
        'Sub_metering_1': np.random.randn(100) * 5 + 2,
        'Sub_metering_2': np.random.randn(100) * 5 + 2,
        'Voltage': np.random.randn(100) * 10 + 240
    })
    # Add some missing values
    df.loc[10:20, 'Global_active_power'] = np.nan
    df.loc[50:55, 'Sub_metering_1'] = np.nan
    return df


class TestDataPreprocessor:
    """Test cases for DataPreprocessor."""
    
    def test_preprocessor_initialization(self):
        """Test preprocessor initialization."""
        preprocessor = DataPreprocessor(scaler_type='standard')
        assert preprocessor.scaler is not None
        assert preprocessor.numeric_columns == []
    
    def test_handle_missing_values(self, dataframe_with_missing):
        """Test missing value handling."""
        preprocessor = DataPreprocessor()
        df = preprocessor.handle_missing_values(dataframe_with_missing)
        
        # Check that no NaN values remain
        assert df.isnull().sum().sum() == 0
        assert len(df) > 0
    
    def test_remove_outliers(self, sample_dataframe):
        """Test outlier removal."""
        # Add some outliers
        sample_dataframe.loc[0, 'Global_active_power'] = 1000
        sample_dataframe.loc[1, 'Global_active_power'] = -1000
        
        preprocessor = DataPreprocessor()
        initial_len = len(sample_dataframe)
        df = preprocessor.remove_outliers(sample_dataframe)
        
        # Check that outliers were removed
        assert len(df) < initial_len
    
    def test_scale_features(self, sample_dataframe):
        """Test feature scaling."""
        preprocessor = DataPreprocessor(scaler_type='standard')
        df = preprocessor.scale_features(sample_dataframe, fit=True)
        
        # Check that features are scaled (mean ~0, std ~1)
        for col in sample_dataframe.columns:
            assert abs(df[col].mean()) < 1.0
            assert abs(df[col].std() - 1.0) < 0.1
    
    def test_full_preprocessing_pipeline(self, dataframe_with_missing):
        """Test full preprocessing pipeline."""
        preprocessor = DataPreprocessor()
        df = preprocessor.preprocess(dataframe_with_missing, fit=True)
        
        # Check that preprocessing was applied
        assert df.isnull().sum().sum() == 0  # No missing values
        assert len(df) < len(dataframe_with_missing)  # Some rows removed


class TestDataShapes:
    """Test data shape preservation."""
    
    def test_preprocessor_preserves_columns(self, sample_dataframe):
        """Test that preprocessor preserves column count."""
        preprocessor = DataPreprocessor()
        initial_cols = len(sample_dataframe.columns)
        df = preprocessor.preprocess(sample_dataframe)
        
        assert len(df.columns) == initial_cols
