"""
Configuration Module
------------------
Configuration settings for the YouTube Automation Tool.
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# YouTube API Key (loaded from .env file)
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

# Maximum results to return for searches
MAX_RESULTS = 50

# Default search parameters
DEFAULT_SEARCH_PARAMS = {
    'max_results': MAX_RESULTS,
    'order': 'viewCount'
}

# Default competitor analysis parameters
DEFAULT_COMPETITOR_PARAMS = {
    'max_results': MAX_RESULTS
}
