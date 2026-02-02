"""Training pipeline script."""
import sys
from pathlib import Path
import pandas as pd
from sklearn.model_selection import train_test_split
import pickle

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.data.loader import load_raw_data, save_processed_data
from src.data.preprocessor import DataPreprocessor
from src.features.engineer import FeatureEngineer
from src.models.trainer import ModelTrainer
from src.visualization.plotter import Plotter
from src.utils.config import DATA_RAW_PATH, DATA_PROCESSED_PATH, MODELS_PATH, TEST_SIZE, VALIDATION_SIZE
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


def main():
    """Run the full training pipeline."""
    logger.info("=" * 50)
    logger.info("Starting Training Pipeline")
    logger.info("=" * 50)
    
    # Step 1: Load raw data
    logger.info("\n[Step 1] Loading raw data...")
    raw_data_path = DATA_RAW_PATH / "household_power_consumption.txt"
    df = load_raw_data(str(raw_data_path))
    
    # Step 2: Preprocess data
    logger.info("\n[Step 2] Preprocessing data...")
    preprocessor = DataPreprocessor()
    df = preprocessor.preprocess(df, fit=True)
    
    # Step 3: Feature engineering
    logger.info("\n[Step 3] Engineering features...")
    engineer = FeatureEngineer()
    df = engineer.engineer_features(df)
    
    # Step 4: Prepare data for modeling
    logger.info("\n[Step 4] Preparing data for modeling...")
    
    # Select target and features
    target_col = 'Global_active_power'
    feature_cols = [col for col in df.columns if col not in [target_col, 'datetime']]
    
    X = df[feature_cols]
    y = df[target_col]
    
    logger.info(f"Features shape: {X.shape}")
    logger.info(f"Target shape: {y.shape}")
    
    # Save processed data
    processed_data = df.copy()
    save_processed_data(processed_data, str(DATA_PROCESSED_PATH / "processed_data.csv"))
    
    # Step 5: Train models
    logger.info("\n[Step 5] Training models...")
    
    # Split data
    X_train, X_temp, y_train, y_temp = train_test_split(
        X, y, test_size=TEST_SIZE + VALIDATION_SIZE, random_state=42
    )
    X_val, X_test, y_val, y_test = train_test_split(
        X_temp, y_temp, test_size=TEST_SIZE / (TEST_SIZE + VALIDATION_SIZE), random_state=42
    )
    
    logger.info(f"Train size: {X_train.shape[0]}, Validation size: {X_val.shape[0]}, Test size: {X_test.shape[0]}")
    
    # Train multiple models and compare
    models = ['linear', 'random_forest', 'gradient_boosting']
    best_model = None
    best_r2 = -np.inf
    
    for model_type in models:
        logger.info(f"\nTraining {model_type} model...")
        
        trainer = ModelTrainer(model_type=model_type)
        trainer.train(X_train, y_train)
        
        # Evaluate on validation set
        val_metrics = trainer.evaluate(X_val, y_val, set_name="Validation")
        
        if val_metrics['r2'] > best_r2:
            best_r2 = val_metrics['r2']
            best_model = trainer
            best_model_type = model_type
    
    # Step 6: Final evaluation on test set
    logger.info(f"\n[Step 6] Final evaluation with {best_model_type} model...")
    test_metrics = best_model.evaluate(X_test, y_test, set_name="Test")
    
    # Step 7: Save model
    logger.info("\n[Step 7] Saving model...")
    model_path = best_model.save_model('power_consumption_model')
    
    # Save preprocessor
    preprocessor_path = Path(MODELS_PATH) / "preprocessor.pkl"
    Path(MODELS_PATH).mkdir(parents=True, exist_ok=True)
    with open(preprocessor_path, 'wb') as f:
        pickle.dump(preprocessor, f)
    logger.info(f"Preprocessor saved to {preprocessor_path}")
    
    # Step 8: Visualization
    logger.info("\n[Step 8] Creating visualizations...")
    plotter = Plotter()
    
    # Plot time series
    if 'datetime' in df.columns:
        df_sorted = df.sort_values('datetime')
        df_sorted.set_index('datetime', inplace=True)
        plotter.plot_time_series(df_sorted, target_col, save=True)
    
    # Plot correlation matrix
    plotter.plot_correlation_matrix(X_train, save=True)
    
    # Plot predictions vs actual
    test_pred = best_model.predict(X_test)
    plotter.plot_predictions_vs_actual(y_test.values, test_pred, save=True)
    
    # Step 9: Summary
    logger.info("\n" + "=" * 50)
    logger.info("Training Pipeline Complete!")
    logger.info("=" * 50)
    logger.info(f"Best Model: {best_model_type}")
    logger.info(f"Test Metrics:")
    logger.info(f"  - R² Score: {test_metrics['r2']:.4f}")
    logger.info(f"  - RMSE: {test_metrics['rmse']:.4f}")
    logger.info(f"  - MAE: {test_metrics['mae']:.4f}")
    logger.info(f"Model saved to: {model_path}")
    logger.info("=" * 50)


if __name__ == '__main__':
    import numpy as np
    main()
