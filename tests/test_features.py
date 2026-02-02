"""Tests for feature engineering."""
import pytest
import pandas as pd
import numpy as np
from src.features.engineer import FeatureEngineer


@pytest.fixture
def sample_timeseries_data():
    """Create sample time series data."""
    np.random.seed(42)
    dates = pd.date_range('2023-01-01', periods=240, freq='H')
    
    df = pd.DataFrame({
        'datetime': dates,
        'Global_active_power': np.random.randn(240).cumsum() + 4,
        'Sub_metering_1': np.random.randn(240) + 2,
        'Voltage': np.random.randn(240) + 240
    })
    
    return df


class TestFeatureEngineer:
    """Test cases for FeatureEngineer."""
    
    def test_engineer_initialization(self):
        """Test feature engineer initialization."""
        engineer = FeatureEngineer()
        assert engineer.engineered_features == []
    
    def test_extract_temporal_features(self, sample_timeseries_data):
        """Test temporal feature extraction."""
        engineer = FeatureEngineer()
        df = engineer.extract_temporal_features(sample_timeseries_data)
        
        # Check that temporal features were added
        expected_features = ['hour', 'day', 'month', 'year', 'day_of_week', 'quarter', 'is_weekend']
        for feature in expected_features:
            assert feature in df.columns
    
    def test_create_rolling_features(self, sample_timeseries_data):
        """Test rolling feature creation."""
        engineer = FeatureEngineer()
        df = engineer.create_rolling_features(
            sample_timeseries_data,
            'Global_active_power',
            windows=[24]
        )
        
        # Check that rolling features were added
        assert 'Global_active_power_rolling_mean_24' in df.columns
        assert 'Global_active_power_rolling_std_24' in df.columns
    
    def test_create_lag_features(self, sample_timeseries_data):
        """Test lag feature creation."""
        engineer = FeatureEngineer()
        df = engineer.create_lag_features(
            sample_timeseries_data,
            'Global_active_power',
            lags=[1]
        )
        
        # Check that lag features were added
        assert 'Global_active_power_lag_1' in df.columns
    
    def test_full_feature_engineering_pipeline(self, sample_timeseries_data):
        """Test full feature engineering pipeline."""
        engineer = FeatureEngineer()
        df = engineer.engineer_features(sample_timeseries_data)
        
        # Check that features were engineered and NaN values were handled
        assert df.isnull().sum().sum() == 0
        assert len(df) < len(sample_timeseries_data)  # Some rows dropped due to lag
        assert len(engineer.engineered_features) > 0
    
    def test_engineered_features_tracking(self, sample_timeseries_data):
        """Test that engineered features are properly tracked."""
        engineer = FeatureEngineer()
        df = engineer.engineer_features(sample_timeseries_data)
        
        # Check that engineered features list contains expected features
        assert 'hour' in engineer.engineered_features
        assert 'is_weekend' in engineer.engineered_features
