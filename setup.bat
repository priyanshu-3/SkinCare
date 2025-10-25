@echo off
echo Setting up Skin Cancer Detection Web Application...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed or not in PATH.
    echo Please install Python 3.7+ from https://python.org
    pause
    exit /b 1
)

REM Create virtual environment if it doesn't exist
if not exist ".venv" (
    echo Creating virtual environment...
    python -m venv .venv
    if errorlevel 1 (
        echo Failed to create virtual environment.
        pause
        exit /b 1
    )
) else (
    echo Virtual environment already exists.
)

REM Activate virtual environment
echo Activating virtual environment...
call .venv\Scripts\activate.bat

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install requirements
echo Installing requirements...
pip install -r requirements.txt
if errorlevel 1 (
    echo Failed to install requirements.
    pause
    exit /b 1
)

REM Create .env file if it doesn't exist
if not exist ".env" (
    echo Creating .env template file...
    echo # Roboflow API Key > .env
    echo ROBOFLOW_API_KEY=your-roboflow-api-key-here >> .env
    echo. >> .env
    echo # Model details >> .env
    echo WORKSPACE=your-workspace-name >> .env
    echo PROJECT=your-project-name >> .env
    echo VERSION=your-version-number >> .env
    echo. >> .env
    echo # Groq API Key ^(from https://console.groq.com/^) >> .env
    echo GROQ_API_KEY=your-groq-api-key-here >> .env
    echo.
    echo IMPORTANT: Please edit the .env file with your actual API keys!
    echo 1. Get Roboflow API key from: https://roboflow.com
    echo 2. Get Groq API key from: https://console.groq.com
    echo.
)

REM Create necessary directories
if not exist "static\uploads" (
    echo Creating upload directories...
    mkdir static\uploads 2>nul
)

echo.
echo Setup completed successfully!
echo.
echo Next steps:
echo 1. Edit .env file with your API keys
echo 2. Run 'run.bat' to start the application
echo.
pause