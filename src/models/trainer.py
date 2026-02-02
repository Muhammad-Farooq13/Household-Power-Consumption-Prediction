"""Model training and evaluation utilities."""
import pandas as pd
import numpy as np
import pickle
from pathlib import Path
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from typing import Tuple, Dict, Any
from src.utils.logger import setup_logger
from src.utils.config import RANDOM_STATE, TEST_SIZE, VALIDATION_SIZE, MODELS_PATH

logger = setup_logger(__name__)


class ModelTrainer:
    """Handles model training and evaluation."""
    
    def __init__(self, model_type: str = 'random_forest'):
        """
        Initialize model trainer.
        
        Args:
            model_type: Type of model ('linear', 'random_forest', 'gradient_boosting')
        """
        self.model_type = model_type
        self.model = self._initialize_model()
        self.scaler = None
        
    def _initialize_model(self) -> Any:
        """Initialize the model based on model_type."""
        models = {
            'linear': LinearRegression(),
            'random_forest': RandomForestRegressor(
                n_estimators=100,
                max_depth=20,
                random_state=RANDOM_STATE,
                n_jobs=-1
            ),
            'gradient_boosting': GradientBoostingRegressor(
                n_estimators=100,
                learning_rate=0.1,
                max_depth=5,
                random_state=RANDOM_STATE
            )
        }
        
        if self.model_type not in models:
            logger.error(f"Unknown model type: {self.model_type}")
            raise ValueError(f"Unknown model type: {self.model_type}")
        
        logger.info(f"Initialized {self.model_type} model")
        return models[self.model_type]
    
    def train_test_split_data(
        self,
        X: pd.DataFrame,
        y: pd.Series,
        test_size: float = TEST_SIZE
    ) -> Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
        """
        Split data into train and test sets.
        
        Args:
            X: Features dataframe
            y: Target series
            test_size: Proportion of test set
        
        Returns:
            X_train, X_test, y_train, y_test
        """
        logger.info(f"Splitting data with test_size={test_size}")
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y,
            test_size=test_size,
            random_state=RANDOM_STATE
        )
        
        logger.info(f"Train set size: {X_train.shape[0]}, Test set size: {X_test.shape[0]}")
        return X_train, X_test, y_train, y_test
    
    def train(self, X_train: pd.DataFrame, y_train: pd.Series) -> None:
        """
        Train the model.
        
        Args:
            X_train: Training features
            y_train: Training target
        """
        logger.info(f"Training {self.model_type} model")
        
        self.model.fit(X_train, y_train)
        
        # Calculate training score
        train_pred = self.model.predict(X_train)
        train_r2 = r2_score(y_train, train_pred)
        
        logger.info(f"Model trained. Training R² score: {train_r2:.4f}")
    
    def evaluate(
        self,
        X_test: pd.DataFrame,
        y_test: pd.Series,
        set_name: str = "Test"
    ) -> Dict[str, float]:
        """
        Evaluate model on test data.
        
        Args:
            X_test: Test features
            y_test: Test target
            set_name: Name of the set (for logging)
        
        Returns:
            Dictionary of evaluation metrics
        """
        logger.info(f"Evaluating on {set_name} set")
        
        predictions = self.model.predict(X_test)
        
        mse = mean_squared_error(y_test, predictions)
        mae = mean_absolute_error(y_test, predictions)
        rmse = np.sqrt(mse)
        r2 = r2_score(y_test, predictions)
        
        metrics = {
            'mse': mse,
            'rmse': rmse,
            'mae': mae,
            'r2': r2
        }
        
        logger.info(f"{set_name} Metrics - RMSE: {rmse:.4f}, MAE: {mae:.4f}, R²: {r2:.4f}")
        
        return metrics
    
    def save_model(self, model_name: str) -> str:
        """
        Save trained model to disk.
        
        Args:
            model_name: Name of the model file (without extension)
        
        Returns:
            Path to saved model
        """
        Path(MODELS_PATH).mkdir(parents=True, exist_ok=True)
        
        model_path = Path(MODELS_PATH) / f"{model_name}.pkl"
        
        with open(model_path, 'wb') as f:
            pickle.dump(self.model, f)
        
        logger.info(f"Model saved to {model_path}")
        return str(model_path)
    
    def load_model(self, model_path: str) -> None:
        """
        Load model from disk.
        
        Args:
            model_path: Path to model file
        """
        with open(model_path, 'rb') as f:
            self.model = pickle.load(f)
        
        logger.info(f"Model loaded from {model_path}")
    
    def predict(self, X: pd.DataFrame) -> np.ndarray:
        """
        Make predictions.
        
        Args:
            X: Features for prediction
        
        Returns:
            Array of predictions
        """
        return self.model.predict(X)
