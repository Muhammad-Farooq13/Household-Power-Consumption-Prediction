#!/bin/bash

# Set up the development environment

echo "Setting up Household Power Consumption project..."

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Create necessary directories
mkdir -p logs
mkdir -p visualizations
mkdir -p mlops_reports

echo "Setup complete!"
echo ""
echo "Next steps:"
echo "1. Place your dataset in data/raw/"
echo "2. Run: python train_pipeline.py"
echo "3. Run: python flask_app.py"
echo "4. Visit: http://localhost:5000"
