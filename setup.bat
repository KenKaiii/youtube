@echo off
:: Setup script for YouTube Automation Tool (Windows)

echo YouTube Automation Tool Setup
echo ============================
echo.

:: Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is not installed or not in PATH. Please install Python and try again.
    exit /b 1
)

:: Create virtual environment
echo Creating virtual environment...
python -m venv venv

:: Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

:: Install dependencies
echo Installing dependencies...
pip install --upgrade pip
pip install -r requirements.txt

:: Create exports directory
echo Creating exports directory...
if not exist exports mkdir exports

:: Prompt for API key
echo.
echo You need a YouTube Data API key to use this tool.
echo You can get one from the Google Cloud Console: https://console.cloud.google.com/
echo.
set /p api_key=Enter your YouTube API key (or press Enter to skip): 

:: Create .env file if API key was provided
if not "%api_key%"=="" (
    echo Creating .env file with your API key...
    echo # YouTube API Key > .env
    echo YOUTUBE_API_KEY=%api_key% >> .env
    echo API key saved to .env file successfully.
) else (
    echo No API key provided. You'll need to create a .env file manually before using the tool.
    echo See .env.example for the required format.
)

echo.
echo Setup complete! You can now run the tool with:
echo   venv\Scripts\activate.bat  # Activate the virtual environment
echo   python main.py             # Run the main tool
echo.
echo To test your API connection first:
echo   python test_api.py
echo.

pause
