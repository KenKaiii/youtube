"""
Export Utilities Module
---------------------
Functions for exporting YouTube data to various formats.
"""
import csv
import json
import os
from datetime import datetime
from terminal_colors import print_success, print_error, print_warning, colored

def export_to_csv(data, filename=None, data_type='videos'):
    """
    Export data to a CSV file.
    
    Args:
        data (list): List of dictionaries containing the data
        filename (str): Optional filename, if None a default name will be generated
        data_type (str): Type of data ('videos' or 'competitors')
        
    Returns:
        str: Path to the exported file
    """
    if not data:
        print_warning("No data to export.")
        return None
    
    # Generate filename if not provided
    if not filename:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{data_type}_{timestamp}.csv"
    
    # Ensure the filename has .csv extension
    if not filename.endswith('.csv'):
        filename += '.csv'
    
    # Create exports directory if it doesn't exist
    os.makedirs('exports', exist_ok=True)
    filepath = os.path.join('exports', filename)
    
    try:
        with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
            if data_type == 'videos':
                # Create a copy of the data for processing
                processed_data = data.copy()
                
                # Process data to add performance metric and format date
                for item in processed_data:
                    # Convert published date to human-readable format (dd/mm/yyyy)
                    if 'published_at' in item:
                        published_date = item['published_at'].split('T')[0]  # Extract YYYY-MM-DD
                        date_parts = published_date.split('-')
                        if len(date_parts) == 3:
                            item['published_date'] = f"{date_parts[2]}/{date_parts[1]}/{date_parts[0]}"  # DD/MM/YYYY
                    
                    # Calculate performance metric (Likes / Views) * 100 - percentage of viewers who liked
                    if 'view_count' in item and 'like_count' in item:
                        views = item['view_count'] if item['view_count'] > 0 else 1  # Avoid division by zero
                        item['performance_score'] = (item['like_count'] / views) * 100
                    
                    # Add URL field for each video
                    if 'video_id' in item and 'url' not in item:
                        item['url'] = f"https://www.youtube.com/watch?v={item['video_id']}"
                
                fieldnames = [
                    'video_id', 'title', 'channel_title', 'published_date', 'published_at',
                    'view_count', 'like_count', 'comment_count', 'performance_score',
                    'url'
                ]
            elif data_type == 'competitors':
                fieldnames = [
                    'channel_id', 'channel_title', 'subscriber_count',
                    'video_count', 'view_count', 'engagement_score', 'relevance_score'
                ]
            else:
                # Use all keys from the first item as fieldnames
                fieldnames = data[0].keys()
            
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, extrasaction='ignore')
            writer.writeheader()
            
            for item in processed_data if data_type == 'videos' else data:
                writer.writerow(item)
        
        return filepath
    
    except Exception as e:
        print_error(f"Error exporting data to CSV: {e}")
        return None

def export_to_json(data, filename=None, data_type='videos'):
    """
    Export data to a JSON file.
    
    Args:
        data (list): List of dictionaries containing the data
        filename (str): Optional filename, if None a default name will be generated
        data_type (str): Type of data ('videos' or 'competitors')
        
    Returns:
        str: Path to the exported file
    """
    if not data:
        print_warning("No data to export.")
        return None
    
    # Generate filename if not provided
    if not filename:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{data_type}_{timestamp}.json"
    
    # Ensure the filename has .json extension
    if not filename.endswith('.json'):
        filename += '.json'
    
    # Create exports directory if it doesn't exist
    os.makedirs('exports', exist_ok=True)
    filepath = os.path.join('exports', filename)
    
    try:
        # Process data for JSON export
        processed_data = data.copy()
        
        if data_type == 'videos':
            # Add performance metric and format date for videos
            for item in processed_data:
                # Convert published date to human-readable format (dd/mm/yyyy)
                if 'published_at' in item:
                    published_date = item['published_at'].split('T')[0]  # Extract YYYY-MM-DD
                    date_parts = published_date.split('-')
                    if len(date_parts) == 3:
                        item['published_date'] = f"{date_parts[2]}/{date_parts[1]}/{date_parts[0]}"  # DD/MM/YYYY
                
                # Calculate performance metric (Likes / Views) * 100 - percentage of viewers who liked
                if 'view_count' in item and 'like_count' in item:
                    views = item['view_count'] if item['view_count'] > 0 else 1  # Avoid division by zero
                    item['performance_score'] = (item['like_count'] / views) * 100
                    
                    # Add performance rating
                    if item['performance_score'] >= 5:  # 5% or more likes-to-views is excellent engagement
                        item['performance_rating'] = "MAKE THIS VIDEO NOW"
                    elif item['performance_score'] >= 2:  # 2-5% likes-to-views is good engagement
                        item['performance_rating'] = "Great"
                    else:  # Less than 2% likes-to-views is lower engagement
                        item['performance_rating'] = "Not the best"
                
                # Add URL field for each video
                if 'video_id' in item and 'url' not in item:
                    item['url'] = f"https://www.youtube.com/watch?v={item['video_id']}"
        
        with open(filepath, 'w', encoding='utf-8') as jsonfile:
            json.dump(processed_data, jsonfile, indent=2)
        
        return filepath
    
    except Exception as e:
        print_error(f"Error exporting data to JSON: {e}")
        return None
