@echo off
echo Starting Skin Cancer Detection Web Application...
echo.

REM Check if virtual environment exists
if not exist ".venv\Scripts\activate.bat" (
    echo Virtual environment not found. Please run setup first.
    pause
    exit /b 1
)

REM Activate virtual environment
call .venv\Scripts\activate.bat

REM Install/update requirements
echo Installing/updating requirements...
pip install -r requirements.txt

REM Check if .env file exists and has required keys
if not exist ".env" (
    echo .env file not found. Please create it with your API keys.
    pause
    exit /b 1
)

REM Start the Flask application
echo.
echo Starting Flask application on http://localhost:5000
echo Press Ctrl+C to stop the server
echo.
python app.py