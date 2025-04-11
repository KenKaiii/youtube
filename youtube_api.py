"""
YouTube API Module
-----------------
Handles interactions with the YouTube Data API.
"""
import os
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from config import YOUTUBE_API_KEY

class YouTubeAPI:
    """Class to handle YouTube API operations."""
    
    def __init__(self, api_key=None):
        """Initialize the YouTube API client."""
        self.api_key = api_key or YOUTUBE_API_KEY
        self.youtube = build('youtube', 'v3', developerKey=self.api_key)
    
    def search_videos(self, query, published_after=None, published_before=None, max_results=50):
        """
        Search for videos based on a query and date range.
        
        Args:
            query (str): The search term
            published_after (str): Start date in ISO format (YYYY-MM-DDThh:mm:ssZ)
            published_before (str): End date in ISO format (YYYY-MM-DDThh:mm:ssZ)
            max_results (int): Maximum number of results to return
            
        Returns:
            list: List of video search results
        """
        try:
            # Build search parameters
            search_params = {
                'q': query,
                'type': 'video',
                'part': 'id,snippet',
                'maxResults': max_results,
                'regionCode': 'US',
                'relevanceLanguage': 'en',  # Filter for English language videos
                'order': 'viewCount'
            }
            
            # Add date filters if provided
            if published_after:
                search_params['publishedAfter'] = published_after
            if published_before:
                search_params['publishedBefore'] = published_before
            
            # Execute search request
            search_response = self.youtube.search().list(**search_params).execute()
            
            # Extract video IDs for additional details
            video_ids = [item['id']['videoId'] for item in search_response.get('items', [])]
            
            if not video_ids:
                return []
            
            # Get detailed video information
            videos_response = self.youtube.videos().list(
                part='snippet,statistics',
                id=','.join(video_ids)
            ).execute()
            
            # Process and return results
            results = []
            for item in videos_response.get('items', []):
                video_data = {
                    'video_id': item['id'],
                    'title': item['snippet']['title'],
                    'description': item['snippet']['description'],
                    'channel_id': item['snippet']['channelId'],
                    'channel_title': item['snippet']['channelTitle'],
                    'published_at': item['snippet']['publishedAt'],
                    'view_count': int(item['statistics'].get('viewCount', 0)),
                    'like_count': int(item['statistics'].get('likeCount', 0)),
                    'comment_count': int(item['statistics'].get('commentCount', 0))
                }
                results.append(video_data)
            
            # Sort by view count (descending)
            results.sort(key=lambda x: x['view_count'], reverse=True)
            return results
            
        except HttpError as e:
            print(f"An HTTP error occurred: {e.resp.status} {e.content}")
            return []
        except Exception as e:
            print(f"An error occurred: {e}")
            return []
    
    def get_channel_details(self, channel_id):
        """
        Get detailed information about a YouTube channel.
        
        Args:
            channel_id (str): The YouTube channel ID
            
        Returns:
            dict: Channel details or None if not found
        """
        try:
            response = self.youtube.channels().list(
                part='snippet,statistics,contentDetails',
                id=channel_id
            ).execute()
            
            if not response.get('items'):
                return None
            
            channel_data = response['items'][0]
            return {
                'channel_id': channel_data['id'],
                'channel_title': channel_data['snippet']['title'],
                'description': channel_data['snippet']['description'],
                'published_at': channel_data['snippet']['publishedAt'],
                'subscriber_count': int(channel_data['statistics'].get('subscriberCount', 0)),
                'video_count': int(channel_data['statistics'].get('videoCount', 0)),
                'view_count': int(channel_data['statistics'].get('viewCount', 0))
            }
            
        except HttpError as e:
            print(f"An HTTP error occurred: {e.resp.status} {e.content}")
            return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
