"""Main Flask application for serving the power consumption model."""
import os
import pickle
import numpy as np
import pandas as pd
from flask import Flask, request, jsonify
from pathlib import Path
from src.utils.logger import setup_logger
from src.utils.config import FLASK_HOST, FLASK_PORT, MODELS_PATH

logger = setup_logger(__name__)

app = Flask(__name__)

# Global variables for model and preprocessor
model = None
preprocessor = None


def load_model_and_preprocessor():
    """Load model and preprocessor from disk."""
    global model, preprocessor
    
    try:
        # Load model
        model_path = Path(MODELS_PATH) / "power_consumption_model.pkl"
        if model_path.exists():
            with open(model_path, 'rb') as f:
                model = pickle.load(f)
            logger.info(f"Model loaded from {model_path}")
        else:
            logger.warning(f"Model not found at {model_path}")
        
        # Load preprocessor
        preprocessor_path = Path(MODELS_PATH) / "preprocessor.pkl"
        if preprocessor_path.exists():
            with open(preprocessor_path, 'rb') as f:
                preprocessor = pickle.load(f)
            logger.info(f"Preprocessor loaded from {preprocessor_path}")
        else:
            logger.warning(f"Preprocessor not found at {preprocessor_path}")
    
    except Exception as e:
        logger.error(f"Error loading model/preprocessor: {str(e)}")


@app.route('/', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'message': 'Power Consumption Model API is running'
    }), 200


@app.route('/predict', methods=['POST'])
def predict():
    """
    Prediction endpoint.
    
    Expected JSON format:
    {
        "features": [[val1, val2, ...], [val1, val2, ...]]
    }
    """
    try:
        if model is None:
            return jsonify({'error': 'Model not loaded'}), 500
        
        data = request.get_json()
        
        if 'features' not in data:
            return jsonify({'error': 'Missing "features" field'}), 400
        
        features = np.array(data['features'])
        
        # Make prediction
        predictions = model.predict(features)
        
        return jsonify({
            'predictions': predictions.tolist(),
            'status': 'success'
        }), 200
    
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        return jsonify({'error': str(e)}), 400


@app.route('/predict-single', methods=['POST'])
def predict_single():
    """
    Single prediction endpoint for a single sample.
    
    Expected JSON format:
    {
        "features": [val1, val2, ...]
    }
    """
    try:
        if model is None:
            return jsonify({'error': 'Model not loaded'}), 500
        
        data = request.get_json()
        
        if 'features' not in data:
            return jsonify({'error': 'Missing "features" field'}), 400
        
        features = np.array(data['features']).reshape(1, -1)
        
        # Make prediction
        prediction = model.predict(features)[0]
        
        return jsonify({
            'prediction': float(prediction),
            'status': 'success'
        }), 200
    
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        return jsonify({'error': str(e)}), 400


@app.route('/model-info', methods=['GET'])
def model_info():
    """Get information about the loaded model."""
    try:
        if model is None:
            return jsonify({'error': 'Model not loaded'}), 500
        
        return jsonify({
            'model_type': type(model).__name__,
            'status': 'loaded',
            'message': 'Model is ready for predictions'
        }), 200
    
    except Exception as e:
        logger.error(f"Error getting model info: {str(e)}")
        return jsonify({'error': str(e)}), 400


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({'error': 'Endpoint not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    logger.error(f"Internal server error: {str(error)}")
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    # Load model and preprocessor before starting the app
    load_model_and_preprocessor()
    
    # Start Flask app
    app.run(host=FLASK_HOST, port=FLASK_PORT, debug=os.getenv('FLASK_DEBUG', False))
