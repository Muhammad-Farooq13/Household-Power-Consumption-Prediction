#!/usr/bin/env python
"""Script to evaluate the trained model on a test dataset."""

import sys
from pathlib import Path
import pandas as pd
import pickle
import numpy as np

sys.path.insert(0, str(Path(__file__).parent))

from src.data.loader import load_processed_data
from src.models.trainer import ModelTrainer
from src.visualization.plotter import Plotter
from src.utils.config import MODELS_PATH, DATA_PROCESSED_PATH
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


def main():
    """Evaluate the trained model."""
    logger.info("=" * 50)
    logger.info("Starting Model Evaluation")
    logger.info("=" * 50)
    
    # Load processed data
    logger.info("\nLoading processed data...")
    try:
        df = load_processed_data(str(DATA_PROCESSED_PATH / "processed_data.csv"))
    except FileNotFoundError:
        logger.error("Processed data not found. Run train_pipeline.py first.")
        sys.exit(1)
    
    # Load the trained model
    logger.info("\nLoading trained model...")
    model_path = Path(MODELS_PATH) / "power_consumption_model.pkl"
    try:
        with open(model_path, 'rb') as f:
            model = pickle.load(f)
        logger.info(f"Model loaded: {type(model).__name__}")
    except FileNotFoundError:
        logger.error(f"Model not found at {model_path}. Run train_pipeline.py first.")
        sys.exit(1)
    
    # Prepare data
    target_col = 'Global_active_power'
    feature_cols = [col for col in df.columns if col not in [target_col, 'datetime']]
    
    X = df[feature_cols]
    y = df[target_col]
    
    # Make predictions on entire dataset
    logger.info("\nMaking predictions...")
    predictions = model.predict(X)
    
    # Calculate metrics
    from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
    
    mse = mean_squared_error(y, predictions)
    rmse = np.sqrt(mse)
    mae = mean_absolute_error(y, predictions)
    r2 = r2_score(y, predictions)
    
    logger.info("\n" + "=" * 50)
    logger.info("Model Evaluation Results")
    logger.info("=" * 50)
    logger.info(f"R² Score: {r2:.4f}")
    logger.info(f"RMSE: {rmse:.4f}")
    logger.info(f"MAE: {mae:.4f}")
    logger.info(f"MSE: {mse:.4f}")
    logger.info("=" * 50)
    
    # Visualize results
    logger.info("\nGenerating visualizations...")
    plotter = Plotter()
    plotter.plot_predictions_vs_actual(y.values, predictions)
    
    logger.info("Evaluation complete!")


if __name__ == '__main__':
    main()
