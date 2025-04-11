"""
Competitor Utilities Module
--------------------------
Functions for finding and analyzing YouTube competitors.
"""
from youtube_api import YouTubeAPI
from config import MAX_RESULTS

def find_competitors(niche_keyword, published_after=None, published_before=None, max_results=None):
    """
    Find top competitors in a niche based on a keyword.
    
    Args:
        niche_keyword (str): The niche keyword to search for
        published_after (str): Start date in ISO format
        published_before (str): End date in ISO format
        max_results (int): Maximum number of results to return
        
    Returns:
        list: List of competitor channels sorted by relevance and engagement
    """
    if max_results is None:
        max_results = MAX_RESULTS
    
    api = YouTubeAPI()
    
    # First, search for top videos in the niche
    videos = api.search_videos(
        query=niche_keyword,
        published_after=published_after,
        published_before=published_before,
        max_results=max_results * 2  # Get more videos to find more channels
    )
    
    # Extract unique channels from videos
    channel_ids = {}
    for video in videos:
        channel_id = video['channel_id']
        if channel_id not in channel_ids:
            channel_ids[channel_id] = {
                'video_count': 1,
                'total_views': video['view_count'],
                'total_likes': video['like_count'],
                'total_comments': video['comment_count']
            }
        else:
            channel_ids[channel_id]['video_count'] += 1
            channel_ids[channel_id]['total_views'] += video['view_count']
            channel_ids[channel_id]['total_likes'] += video['like_count']
            channel_ids[channel_id]['total_comments'] += video['comment_count']
    
    # Get detailed information for each channel
    competitors = []
    for channel_id, stats in channel_ids.items():
        channel_details = api.get_channel_details(channel_id)
        if channel_details:
            # Calculate engagement score
            engagement_score = 0
            if stats['total_views'] > 0:
                engagement_score = (stats['total_likes'] + stats['total_comments']) / stats['total_views']
            
            # Add relevance score based on video count in search results
            relevance_score = stats['video_count'] / len(videos) if videos else 0
            
            # Combine channel details with calculated metrics
            competitor = {
                **channel_details,
                'videos_in_results': stats['video_count'],
                'engagement_score': engagement_score,
                'relevance_score': relevance_score,
                'combined_score': engagement_score * 0.7 + relevance_score * 0.3  # Weighted score
            }
            competitors.append(competitor)
    
    # Sort by combined score (descending)
    competitors.sort(key=lambda x: x['combined_score'], reverse=True)
    
    # Return top competitors up to max_results
    return competitors[:max_results]

def analyze_competitor(channel_id):
    """
    Perform detailed analysis of a competitor channel.
    
    Args:
        channel_id (str): YouTube channel ID
        
    Returns:
        dict: Detailed analysis of the competitor
    """
    api = YouTubeAPI()
    
    # Get channel details
    channel = api.get_channel_details(channel_id)
    if not channel:
        return None
    
    # Get recent videos from the channel
    try:
        # Get channel's uploads playlist ID
        channels_response = api.youtube.channels().list(
            part='contentDetails',
            id=channel_id
        ).execute()
        
        if not channels_response.get('items'):
            return channel
        
        uploads_playlist_id = channels_response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
        
        # Get recent videos from uploads playlist
        playlist_response = api.youtube.playlistItems().list(
            part='snippet',
            playlistId=uploads_playlist_id,
            maxResults=10
        ).execute()
        
        video_ids = [item['snippet']['resourceId']['videoId'] 
                    for item in playlist_response.get('items', [])]
        
        if not video_ids:
            return channel
        
        # Get video details
        videos_response = api.youtube.videos().list(
            part='snippet,statistics',
            id=','.join(video_ids)
        ).execute()
        
        videos = []
        for item in videos_response.get('items', []):
            video = {
                'video_id': item['id'],
                'title': item['snippet']['title'],
                'published_at': item['snippet']['publishedAt'],
                'view_count': int(item['statistics'].get('viewCount', 0)),
                'like_count': int(item['statistics'].get('likeCount', 0)),
                'comment_count': int(item['statistics'].get('commentCount', 0))
            }
            videos.append(video)
        
        # Calculate metrics
        total_views = sum(video['view_count'] for video in videos)
        total_likes = sum(video['like_count'] for video in videos)
        total_comments = sum(video['comment_count'] for video in videos)
        
        # Add analysis to channel data
        channel['recent_videos'] = videos
        channel['recent_videos_count'] = len(videos)
        channel['recent_videos_avg_views'] = total_views / len(videos) if videos else 0
        channel['recent_videos_engagement'] = (total_likes + total_comments) / total_views if total_views > 0 else 0
        
        return channel
        
    except Exception as e:
        print(f"Error analyzing competitor: {e}")
        return channel
