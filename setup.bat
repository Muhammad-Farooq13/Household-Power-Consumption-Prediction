@echo off
REM Set up the development environment for Windows

echo Setting up Household Power Consumption project...

REM Create virtual environment
python -m venv venv
call venv\Scripts\activate.bat

REM Install dependencies
python -m pip install --upgrade pip
pip install -r requirements.txt

REM Create necessary directories
if not exist logs mkdir logs
if not exist visualizations mkdir visualizations
if not exist mlops_reports mkdir mlops_reports

echo.
echo Setup complete!
echo.
echo Next steps:
echo 1. Place your dataset in data\raw\
echo 2. Run: python train_pipeline.py
echo 3. Run: python flask_app.py
echo 4. Visit: http://localhost:5000
