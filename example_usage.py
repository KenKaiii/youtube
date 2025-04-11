#!/usr/bin/env python3
"""
Example Usage Script
-------------------
Demonstrates how to use the YouTube Automation Tool as a module in other Python scripts.
"""
from datetime import datetime, timedelta
from search_utils import search_top_videos
from competitor_utils import find_competitors, analyze_competitor
from export_utils import export_to_csv, export_to_json
from terminal_colors import (
    print_header, print_section, print_result_item, print_success, 
    print_error, print_info, print_warning, print_loading, 
    colored, create_border_box
)

def example_search():
    """Example of searching for top videos."""
    print_header("Example: Searching for Top Videos", width=70, color='bright_magenta')
    
    # Define search parameters
    search_term = "python tutorial"
    days = 7
    
    # Calculate date range
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    start_date_str = start_date.strftime('%Y-%m-%dT%H:%M:%SZ')
    end_date_str = end_date.strftime('%Y-%m-%dT%H:%M:%SZ')
    
    print_loading(f"Searching for: \"{colored(search_term, 'bright_cyan')}\" in the last {colored(days, 'bright_yellow')} days...")
    
    # Perform search
    results = search_top_videos(
        query=search_term,
        published_after=start_date_str,
        published_before=end_date_str,
        max_results=5  # Limit to 5 results for this example
    )
    
    # Display results
    if results:
        print_success(f"Found {colored(len(results), 'bright_green')} videos:")
        
        for i, video in enumerate(results, 1):
            details = {
                "Channel": video['channel_title'],
                "Views": f"{video['view_count']:,}",
                "URL": f"https://www.youtube.com/watch?v={video['video_id']}"
            }
            print_result_item(i, video['title'], details)
        
        # Export results
        export_path = export_to_json(results, filename="example_search_results.json", data_type="videos")
        print_info(f"Results exported to: {colored(export_path, 'bright_cyan')}")
    else:
        print_warning("No videos found matching the criteria.")

def example_competitor_analysis():
    """Example of finding and analyzing competitors."""
    print_header("Example: Finding Competitors", width=70, color='bright_blue')
    
    # Define search parameters
    niche_keyword = "data science"
    days = 30
    
    # Calculate date range
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    start_date_str = start_date.strftime('%Y-%m-%dT%H:%M:%SZ')
    end_date_str = end_date.strftime('%Y-%m-%dT%H:%M:%SZ')
    
    print_loading(f"Finding competitors for: \"{colored(niche_keyword, 'bright_cyan')}\" active in the last {colored(days, 'bright_yellow')} days...")
    
    # Find competitors
    competitors = find_competitors(
        niche_keyword=niche_keyword,
        published_after=start_date_str,
        published_before=end_date_str,
        max_results=3  # Limit to 3 results for this example
    )
    
    # Display results
    if competitors:
        print_success(f"Found {colored(len(competitors), 'bright_green')} competitors:")
        
        for i, competitor in enumerate(competitors, 1):
            details = {
                "Subscribers": f"{competitor['subscriber_count']:,}",
                "Total Videos": competitor['video_count'],
                "Channel URL": f"https://www.youtube.com/channel/{competitor['channel_id']}"
            }
            print_result_item(i, competitor['channel_title'], details)
        
        # Export results
        export_path = export_to_csv(competitors, filename="example_competitors.csv", data_type="competitors")
        print_info(f"Results exported to: {colored(export_path, 'bright_cyan')}")
        
        # Detailed analysis of the top competitor
        if len(competitors) > 0:
            print_section("Detailed Analysis of Top Competitor")
            top_competitor = competitors[0]
            detailed_analysis = analyze_competitor(top_competitor['channel_id'])
            
            if detailed_analysis and 'recent_videos' in detailed_analysis:
                analysis_info = f"""
Channel: {colored(detailed_analysis['channel_title'], 'bright_white')}
Subscribers: {colored(f"{detailed_analysis['subscriber_count']:,}", 'bright_yellow')}
Recent Videos: {colored(detailed_analysis['recent_videos_count'], 'bright_green')}
Average Views: {colored(f"{int(detailed_analysis['recent_videos_avg_views']):,}", 'bright_cyan')}
"""
                print(create_border_box(analysis_info, color='blue'))
                
                if detailed_analysis['recent_videos']:
                    print_section("Recent Videos")
                    for i, video in enumerate(detailed_analysis['recent_videos'][:3], 1):
                        print(f" {colored(i, 'bright_green')}. {colored(video['title'], 'white')} - {colored(f"{video['view_count']:,}", 'bright_yellow')} views")
    else:
        print_warning("No competitors found matching the criteria.")

def main():
    """Run the example usage demonstrations."""
    print_header("YouTube Automation Tool - Example Usage", width=70, color='bright_red')
    
    # Example 1: Search for top videos
    example_search()
    
    # Example 2: Find and analyze competitors
    example_competitor_analysis()
    
    print_success("Examples completed. Check the exports directory for the exported files.")

if __name__ == "__main__":
    main()
