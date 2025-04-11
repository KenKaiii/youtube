"""
Search Utilities Module
----------------------
Functions for searching and analyzing YouTube videos.
"""
from youtube_api import YouTubeAPI
from config import MAX_RESULTS

def search_top_videos(query, published_after=None, published_before=None, max_results=None):
    """
    Search for top videos based on a query and date range.
    
    Args:
        query (str): The search term
        published_after (str): Start date in ISO format
        published_before (str): End date in ISO format
        max_results (int): Maximum number of results to return
        
    Returns:
        list: List of top videos sorted by view count
    """
    if max_results is None:
        max_results = MAX_RESULTS
    
    api = YouTubeAPI()
    results = api.search_videos(
        query=query,
        published_after=published_after,
        published_before=published_before,
        max_results=max_results
    )
    
    return results

def analyze_video_metrics(videos):
    """
    Analyze video metrics to extract insights.
    
    Args:
        videos (list): List of video data dictionaries
        
    Returns:
        dict: Analysis results including averages and trends
    """
    if not videos:
        return {
            'total_videos': 0,
            'avg_views': 0,
            'avg_likes': 0,
            'avg_comments': 0
        }
    
    total_views = sum(video['view_count'] for video in videos)
    total_likes = sum(video['like_count'] for video in videos)
    total_comments = sum(video['comment_count'] for video in videos)
    
    count = len(videos)
    
    return {
        'total_videos': count,
        'avg_views': total_views / count,
        'avg_likes': total_likes / count,
        'avg_comments': total_comments / count,
        'engagement_rate': (total_likes + total_comments) / total_views if total_views > 0 else 0
    }

def get_video_tags(video_id):
    """
    Get tags for a specific video.
    
    Args:
        video_id (str): YouTube video ID
        
    Returns:
        list: List of tags for the video
    """
    api = YouTubeAPI()
    try:
        response = api.youtube.videos().list(
            part='snippet',
            id=video_id
        ).execute()
        
        if not response.get('items'):
            return []
        
        return response['items'][0]['snippet'].get('tags', [])
    except Exception as e:
        print(f"Error getting video tags: {e}")
        return []
