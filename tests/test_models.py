"""Tests for model training and evaluation."""
import pytest
import pandas as pd
import numpy as np
from src.models.trainer import ModelTrainer


@pytest.fixture
def sample_training_data():
    """Create sample training data."""
    np.random.seed(42)
    n_samples = 100
    n_features = 10
    
    X = pd.DataFrame(
        np.random.randn(n_samples, n_features),
        columns=[f'feature_{i}' for i in range(n_features)]
    )
    y = pd.Series(
        X.iloc[:, 0] * 2 + X.iloc[:, 1] * 1.5 + np.random.randn(n_samples) * 0.1,
        name='target'
    )
    
    return X, y


class TestModelTrainer:
    """Test cases for ModelTrainer."""
    
    def test_linear_model_initialization(self):
        """Test linear model initialization."""
        trainer = ModelTrainer(model_type='linear')
        assert trainer.model is not None
        assert trainer.model_type == 'linear'
    
    def test_random_forest_model_initialization(self):
        """Test random forest model initialization."""
        trainer = ModelTrainer(model_type='random_forest')
        assert trainer.model is not None
        assert trainer.model_type == 'random_forest'
    
    def test_gradient_boosting_model_initialization(self):
        """Test gradient boosting model initialization."""
        trainer = ModelTrainer(model_type='gradient_boosting')
        assert trainer.model is not None
        assert trainer.model_type == 'gradient_boosting'
    
    def test_invalid_model_type(self):
        """Test that invalid model type raises error."""
        with pytest.raises(ValueError):
            ModelTrainer(model_type='invalid_model')
    
    def test_train_test_split(self, sample_training_data):
        """Test train/test split."""
        X, y = sample_training_data
        trainer = ModelTrainer()
        
        X_train, X_test, y_train, y_test = trainer.train_test_split_data(X, y, test_size=0.2)
        
        assert len(X_train) + len(X_test) == len(X)
        assert len(X_test) == int(len(X) * 0.2)
    
    def test_model_training(self, sample_training_data):
        """Test model training."""
        X, y = sample_training_data
        trainer = ModelTrainer(model_type='linear')
        
        X_train, X_test, y_train, y_test = trainer.train_test_split_data(X, y)
        trainer.train(X_train, y_train)
        
        # Make predictions
        predictions = trainer.predict(X_test)
        assert len(predictions) == len(X_test)
    
    def test_model_evaluation(self, sample_training_data):
        """Test model evaluation."""
        X, y = sample_training_data
        trainer = ModelTrainer(model_type='linear')
        
        X_train, X_test, y_train, y_test = trainer.train_test_split_data(X, y)
        trainer.train(X_train, y_train)
        
        metrics = trainer.evaluate(X_test, y_test)
        
        assert 'mse' in metrics
        assert 'rmse' in metrics
        assert 'mae' in metrics
        assert 'r2' in metrics
        assert metrics['r2'] > 0.5  # Should have reasonable fit
    
    def test_predictions_shape(self, sample_training_data):
        """Test that predictions have correct shape."""
        X, y = sample_training_data
        trainer = ModelTrainer(model_type='random_forest')
        
        X_train, X_test, y_train, y_test = trainer.train_test_split_data(X, y)
        trainer.train(X_train, y_train)
        
        predictions = trainer.predict(X_test)
        assert predictions.shape[0] == X_test.shape[0]


class TestMultipleModels:
    """Test comparison of multiple models."""
    
    def test_model_comparison(self, sample_training_data):
        """Test that different models can be trained and compared."""
        X, y = sample_training_data
        models_to_test = ['linear', 'random_forest']
        
        scores = {}
        for model_type in models_to_test:
            trainer = ModelTrainer(model_type=model_type)
            X_train, X_test, y_train, y_test = trainer.train_test_split_data(X, y)
            trainer.train(X_train, y_train)
            metrics = trainer.evaluate(X_test, y_test)
            scores[model_type] = metrics['r2']
        
        # All models should have some predictive power
        assert all(score > 0.3 for score in scores.values())
