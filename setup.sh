#!/bin/bash
# Setup script for YouTube Automation Tool

echo "YouTube Automation Tool Setup"
echo "============================"
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed. Please install Python 3 and try again."
    exit 1
fi

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    # Windows
    echo "Activating virtual environment (Windows)..."
    source venv/Scripts/activate
else
    # Linux/macOS
    echo "Activating virtual environment (Unix)..."
    source venv/bin/activate
fi

# Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Create exports directory
echo "Creating exports directory..."
mkdir -p exports

# Prompt for API key
echo
echo "You need a YouTube Data API key to use this tool."
echo "You can get one from the Google Cloud Console: https://console.cloud.google.com/"
echo
read -p "Enter your YouTube API key (or press Enter to skip): " api_key

# Create .env file if API key was provided
if [ -n "$api_key" ]; then
    echo "Creating .env file with your API key..."
    echo "# YouTube API Key" > .env
    echo "YOUTUBE_API_KEY=$api_key" >> .env
    echo "API key saved to .env file successfully."
else
    echo "No API key provided. You'll need to create a .env file manually before using the tool."
    echo "See .env.example for the required format."
fi

echo
echo "Setup complete! You can now run the tool with:"
echo "  source venv/bin/activate  # Activate the virtual environment"
echo "  python main.py            # Run the main tool"
echo
echo "To test your API connection first:"
echo "  python test_api.py"
echo
