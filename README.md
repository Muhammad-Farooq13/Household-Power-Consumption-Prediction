# Household Power Consumption Prediction

A comprehensive machine learning project for predicting household power consumption using MLOps best practices, Docker deployment, and Flask REST API.

## Table of Contents

- [Project Overview](#project-overview)
- [Dataset](#dataset)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Model Training](#model-training)
- [Flask Deployment](#flask-deployment)
- [Docker Deployment](#docker-deployment)
- [MLOps Pipeline](#mlops-pipeline)
- [Testing](#testing)
- [API Documentation](#api-documentation)
- [Contributing](#contributing)
- [License](#license)

## Project Overview

This project uses machine learning to predict household power consumption based on historical data and temporal features. It includes:

- **Data Processing**: Complete data cleaning and preprocessing pipeline
- **Feature Engineering**: Temporal features, rolling statistics, and lag features
- **Model Training**: Multiple model types (Linear Regression, Random Forest, Gradient Boosting)
- **Model Evaluation**: Comprehensive metrics and visualization
- **Deployment**: Flask REST API and Docker containerization
- **MLOps**: CI/CD pipeline with automated testing and model validation
- **Testing**: Comprehensive unit and integration tests

### Key Technologies

- **Machine Learning**: scikit-learn, pandas, numpy
- **Web Framework**: Flask
- **Containerization**: Docker, Docker Compose
- **CI/CD**: GitHub Actions
- **Testing**: pytest
- **Code Quality**: pylint, black, flake8

## Dataset

### Dataset Description

**Source**: Household Power Consumption Dataset  
**Features**: 
- `Global_active_power`: Global minute-averaged active power (in kilowatt)
- `Global_reactive_power`: Global minute-averaged reactive power (in kilowatt)
- `Voltage`: Minute-averaged voltage (in volt)
- `Global_intensity`: Global minute-averaged current intensity (in ampere)
- `Sub_metering_1`: Energy sub-metering No. 1 (in watt-hour)
- `Sub_metering_2`: Energy sub-metering No. 2 (in watt-hour)
- `Sub_metering_3`: Energy sub-metering No. 3 (in watt-hour)

### Preprocessing Steps

1. **Missing Value Handling**: Forward fill and backward fill for time series data
2. **Outlier Removal**: Standard deviation-based outlier detection and removal
3. **Feature Scaling**: StandardScaler for normalization
4. **Temporal Feature Extraction**: Hour, day, month, year, day of week, quarter, weekend flag
5. **Rolling Features**: 24-hour and 168-hour (weekly) rolling mean and standard deviation
6. **Lag Features**: 1-hour, 24-hour, and 168-hour lag features

## Project Structure

```
household/
├── data/
│   ├── raw/                           # Raw datasets
│   └── processed/                     # Cleaned and processed datasets
├── notebooks/                          # Jupyter notebooks for exploration
├── src/
│   ├── data/
│   │   ├── loader.py                 # Data loading utilities
│   │   └── preprocessor.py           # Data preprocessing pipeline
│   ├── features/
│   │   └── engineer.py               # Feature engineering utilities
│   ├── models/
│   │   └── trainer.py                # Model training and evaluation
│   ├── visualization/
│   │   └── plotter.py                # Visualization utilities
│   └── utils/
│       ├── config.py                 # Project configuration
│       └── logger.py                 # Logging utilities
├── tests/
│   ├── test_data.py                  # Tests for data processing
│   ├── test_models.py                # Tests for model training
│   ├── test_features.py              # Tests for feature engineering
│   ├── test_flask.py                 # Tests for Flask API
│   └── conftest.py                   # pytest configuration
├── models/                            # Trained models (pickle files)
├── logs/                              # Application logs
├── visualizations/                    # Generated plots and visualizations
├── .github/
│   └── workflows/
│       └── ci_cd.yml                 # GitHub Actions CI/CD pipeline
├── flask_app.py                      # Flask REST API
├── train_pipeline.py                 # Complete training pipeline
├── mlops_pipeline.py                 # MLOps pipeline
├── Dockerfile                        # Docker configuration
├── docker-compose.yml                # Docker Compose configuration
├── requirements.txt                  # Python dependencies
├── .gitignore                        # Git ignore file
└── README.md                         # This file
```

## Installation

### Prerequisites

- Python 3.9 or higher
- pip or conda
- Docker (optional, for containerized deployment)

### Local Setup

1. **Clone the repository**:
```bash
git clone https://github.com/yourusername/household-power-consumption.git
cd household-power-consumption
```

2. **Create a virtual environment**:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Place your dataset**:
```bash
# Copy the household_power_consumption.txt file to data/raw/
cp household_power_consumption.txt data/raw/
```

## Usage

### 1. Run the Complete Training Pipeline

```bash
python train_pipeline.py
```

This will:
- Load raw data
- Preprocess the data
- Engineer features
- Train multiple models
- Evaluate and compare models
- Save the best model
- Generate visualizations

### 2. Run Individual Components

**Load and preprocess data**:
```python
from src.data.loader import load_raw_data
from src.data.preprocessor import DataPreprocessor

df = load_raw_data('data/raw/household_power_consumption.txt')
preprocessor = DataPreprocessor()
df_processed = preprocessor.preprocess(df)
```

**Engineer features**:
```python
from src.features.engineer import FeatureEngineer

engineer = FeatureEngineer()
df_engineered = engineer.engineer_features(df_processed)
```

**Train a model**:
```python
from src.models.trainer import ModelTrainer

trainer = ModelTrainer(model_type='random_forest')
trainer.train(X_train, y_train)
metrics = trainer.evaluate(X_test, y_test)
trainer.save_model('my_model')
```

## Model Training

### Supported Models

1. **Linear Regression**: Fast baseline model
2. **Random Forest**: Ensemble method with good generalization
3. **Gradient Boosting**: Advanced ensemble with high accuracy

### Training Configuration

Edit `src/utils/config.py` to customize:

```python
RANDOM_STATE = 42              # Random seed
TEST_SIZE = 0.2                # Test set proportion
VALIDATION_SIZE = 0.2          # Validation set proportion
MISSING_VALUE_THRESHOLD = 0.3  # Threshold for dropping columns
OUTLIER_STD_DEV = 3            # Standard deviations for outlier detection
FEATURE_SCALING = 'standard'   # 'standard' or 'minmax'
```

### Model Performance

The training pipeline will output metrics including:
- **R² Score**: Coefficient of determination
- **RMSE**: Root Mean Squared Error
- **MAE**: Mean Absolute Error

## Flask Deployment

### Running the Flask App Locally

1. **Train the model** (if not already done):
```bash
python train_pipeline.py
```

2. **Start the Flask server**:
```bash
python flask_app.py
```

The server will run at `http://localhost:5000`

### API Endpoints

#### Health Check
```
GET /
```
Response: `{"status": "healthy", "message": "..."}`

#### Get Model Info
```
GET /model-info
```
Response: `{"model_type": "RandomForestRegressor", "status": "loaded"}`

#### Batch Predictions
```
POST /predict
Content-Type: application/json

{
    "features": [
        [feature_1, feature_2, ..., feature_n],
        [feature_1, feature_2, ..., feature_n]
    ]
}
```

Response:
```json
{
    "predictions": [pred_1, pred_2],
    "status": "success"
}
```

#### Single Prediction
```
POST /predict-single
Content-Type: application/json

{
    "features": [feature_1, feature_2, ..., feature_n]
}
```

Response:
```json
{
    "prediction": pred_value,
    "status": "success"
}
```

### Example Request

```bash
curl -X POST http://localhost:5000/predict-single \
  -H "Content-Type: application/json" \
  -d '{"features": [4.2, 0.5, 240.0, 18.0, 0, 0, 1, 0.5, 3.8]}'
```

## Docker Deployment

### Build Docker Image

```bash
docker build -t household-power-api:latest .
```

### Run Container

```bash
docker run -p 5000:5000 \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/models:/app/models \
  household-power-api:latest
```

### Using Docker Compose

```bash
docker-compose up -d
```

This will:
- Build the image
- Start the container
- Mount necessary volumes
- Expose port 5000

### Stop Docker Container

```bash
docker-compose down
```

## MLOps Pipeline

### Running the MLOps Pipeline

```bash
python mlops_pipeline.py
```

### Pipeline Stages

1. **Unit Tests**: Validates data processing, models, and Flask API
2. **Linting**: Code quality checks with pylint
3. **Docker Build**: Builds container image
4. **Integration Tests**: Tests API endpoints

### Automated Testing with GitHub Actions

The CI/CD pipeline runs automatically on:
- Push to `main` or `develop` branches
- Pull requests

**Workflow includes**:
- Tests on Python 3.9, 3.10, 3.11
- Code coverage reporting
- Docker image build
- Linting and code quality checks

## Testing

### Run All Tests

```bash
pytest tests/ -v
```

### Run Tests with Coverage

```bash
pytest tests/ -v --cov=src/
```

### Run Specific Test File

```bash
pytest tests/test_models.py -v
```

### Test Categories

- **test_data.py**: Data loading and preprocessing
- **test_models.py**: Model training and evaluation
- **test_features.py**: Feature engineering
- **test_flask.py**: Flask API endpoints

### Test Coverage

Target: >80% code coverage

```bash
pytest --cov=src/ --cov-report=html
```

## API Documentation

### Request/Response Examples

#### Example 1: Single Prediction

**Request**:
```bash
curl -X POST http://localhost:5000/predict-single \
  -H "Content-Type: application/json" \
  -d '{
    "features": [4.2, 0.5, 240.0, 18.0, 0, 0, 1, 0.5, 3.8]
  }'
```

**Response**:
```json
{
    "prediction": 4.15,
    "status": "success"
}
```

#### Example 2: Batch Predictions

**Request**:
```bash
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "features": [
      [4.2, 0.5, 240.0, 18.0, 0, 0, 1, 0.5, 3.8],
      [3.8, 0.4, 241.0, 17.0, 1, 1, 0, 0.4, 3.5]
    ]
  }'
```

**Response**:
```json
{
    "predictions": [4.15, 3.95],
    "status": "success"
}
```

## Model Versioning

Models are saved with timestamps in the `models/` directory:

```
models/
├── power_consumption_model.pkl    # Current model
├── preprocessor.pkl               # Fitted preprocessor
└── model_20240115_120000.pkl      # Versioned models
```

## Monitoring and Logging

All activities are logged to `logs/` directory:

```
logs/
├── train_pipeline.log
├── flask_app.log
├── mlops_pipeline.log
└── ...
```

## Configuration

### Environment Variables

```bash
export FLASK_DEBUG=False
export FLASK_ENV=production
export LOG_LEVEL=INFO
```

Or create a `.env` file:

```
FLASK_DEBUG=False
FLASK_ENV=production
LOG_LEVEL=INFO
```

## Troubleshooting

### Issue: Model not found

**Solution**: Train the model first with `python train_pipeline.py`

### Issue: Docker build fails

**Solution**: Ensure Docker is running and you have sufficient disk space

### Issue: API returns 400 error

**Solution**: Check that features array has correct length and format

### Issue: Tests fail

**Solution**: Ensure all dependencies are installed with `pip install -r requirements.txt`

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/new-feature`
3. Commit changes: `git commit -am 'Add new feature'`
4. Push to branch: `git push origin feature/new-feature`
5. Submit pull request

### Code Standards

- Follow PEP 8 style guide
- Run linting: `pylint src/`
- Run tests: `pytest tests/`
- Use type hints where possible

## Performance Metrics

### Model Performance (on Test Set)

| Model | R² Score | RMSE | MAE |
|-------|----------|------|-----|
| Linear Regression | ~0.72 | ~1.8 | ~0.85 |
| Random Forest | ~0.85 | ~1.2 | ~0.6 |
| Gradient Boosting | ~0.87 | ~1.1 | ~0.55 |

*Note: Actual values depend on your specific dataset and preprocessing steps*

## Future Improvements

- [ ] Add LSTM/RNN models for sequence prediction
- [ ] Implement real-time predictions with streaming data
- [ ] Add model explainability (SHAP values)
- [ ] Implement A/B testing framework
- [ ] Add model retraining scheduler
- [ ] Implement model monitoring and alerting
- [ ] Add database integration (PostgreSQL)
- [ ] Create web dashboard for visualizations

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Citation

If you use this project in your research or work, please cite:

```bibtex
@software{household_power_2024,
  author = {Muhammad Farooq},
  title = {Household Power Consumption Prediction},
  year = {2024},
  url = {https://github.com/Muhammad-Farooq-13/household-power-consumption}
}
```

## Contact

For questions or support, please create an issue on GitHub or contact mfarooqshafee333@gmail.com

---

**Last Updated**: February 2024  
**Version**: 1.0.0
