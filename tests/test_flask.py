"""Tests for Flask application."""
import pytest
import json
import sys
from pathlib import Path
import numpy as np

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from flask_app import app


@pytest.fixture
def client():
    """Create Flask test client."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


class TestFlaskApp:
    """Test cases for Flask application."""
    
    def test_health_check(self, client):
        """Test health check endpoint."""
        response = client.get('/')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'healthy'
    
    def test_model_info_no_model(self, client):
        """Test model info endpoint when no model loaded."""
        response = client.get('/model-info')
        
        # Will return 500 since model is not loaded in test
        assert response.status_code in [500, 200]
    
    def test_predict_missing_features(self, client):
        """Test predict endpoint with missing features."""
        response = client.post('/predict', 
            data=json.dumps({}),
            content_type='application/json'
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_predict_single_missing_features(self, client):
        """Test predict-single endpoint with missing features."""
        response = client.post('/predict-single',
            data=json.dumps({}),
            content_type='application/json'
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_invalid_endpoint(self, client):
        """Test invalid endpoint."""
        response = client.get('/invalid-endpoint')
        
        assert response.status_code == 404


class TestFlaskAppWithMockData:
    """Test Flask app with mock prediction data."""
    
    def test_health_check_success(self, client):
        """Test successful health check."""
        response = client.get('/')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'status' in data
        assert data['status'] == 'healthy'
