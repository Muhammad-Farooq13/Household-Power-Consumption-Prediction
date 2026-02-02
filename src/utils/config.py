"""Configuration file for the project."""
import os
from pathlib import Path

# Project paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
DATA_RAW_PATH = PROJECT_ROOT / "data" / "raw"
DATA_PROCESSED_PATH = PROJECT_ROOT / "data" / "processed"
NOTEBOOKS_PATH = PROJECT_ROOT / "notebooks"
MODELS_PATH = PROJECT_ROOT / "models"
TESTS_PATH = PROJECT_ROOT / "tests"

# Data configuration
RANDOM_STATE = 42
TEST_SIZE = 0.2
VALIDATION_SIZE = 0.2

# Model configuration
MODEL_NAME = "power_consumption_model"
MODEL_VERSION = "1.0"

# Flask configuration
FLASK_HOST = "0.0.0.0"
FLASK_PORT = 5000
FLASK_DEBUG = os.getenv("FLASK_DEBUG", "False") == "True"

# Logging configuration
LOG_LEVEL = "INFO"
LOG_DIR = PROJECT_ROOT / "logs"

# Data preprocessing parameters
MISSING_VALUE_THRESHOLD = 0.3
OUTLIER_STD_DEV = 3
FEATURE_SCALING = "standard"  # "standard" or "minmax"

# Create necessary directories
os.makedirs(LOG_DIR, exist_ok=True)
