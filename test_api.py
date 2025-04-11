#!/usr/bin/env python3
"""
YouTube API Test Script
----------------------
A simple script to test the YouTube API connection and functionality.
"""
import sys
from youtube_api import YouTubeAPI
from config import YOUTUBE_API_KEY
from terminal_colors import (
    print_header, print_section, print_success, print_error, 
    print_warning, print_info, colored, create_border_box
)

def test_api_connection():
    """Test the YouTube API connection with the provided API key."""
    print_header("YouTube API Connection Test", width=60, color='bright_blue')
    
    if not YOUTUBE_API_KEY:
        print_error("No API key found in .env file.")
        print_info("Please follow the instructions in the README.md file to set up your API key.")
        return False
    
    try:
        api = YouTubeAPI()
        
        # Test a simple search query
        print_info("Testing search functionality...")
        results = api.search_videos(query="test", max_results=1)
        
        if results:
            video = results[0]
            print_success("API connection is working correctly!")
            
            print_section("Sample Video Found")
            video_info = f"""
Title: {colored(video['title'], 'bright_white')}
Channel: {colored(video['channel_title'], 'cyan')}
Views: {colored(f"{video['view_count']:,}", 'bright_yellow')}
URL: {colored(f"https://www.youtube.com/watch?v={video['video_id']}", 'bright_blue')}
"""
            print(create_border_box(video_info, color='green'))
            return True
        else:
            print_warning("API connection successful, but no videos were returned.")
            print_info("This might be due to API quota limitations or search restrictions.")
            return True
            
    except Exception as e:
        print_error(f"Failed to connect to the YouTube API: {e}")
        
        print_section("Possible Issues")
        print(f" {colored('1.', 'bright_red')} Invalid API key")
        print(f" {colored('2.', 'bright_red')} API quota exceeded")
        print(f" {colored('3.', 'bright_red')} Network connectivity issues")
        print(f" {colored('4.', 'bright_red')} Missing dependencies (try running 'pip install -r requirements.txt')")
        return False

if __name__ == "__main__":
    try:
        success = test_api_connection()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print_error("Operation cancelled by user.")
        sys.exit(0)
    except Exception as e:
        print_error(f"An unexpected error occurred: {e}")
        sys.exit(1)
