#!/usr/bin/env python3
"""
Batch Processing Script
---------------------
Demonstrates how to use the YouTube Automation Tool for batch processing multiple searches.
"""
import sys
import time
from datetime import datetime, timedelta
import json
from search_utils import search_top_videos
from competitor_utils import find_competitors
from export_utils import export_to_csv, export_to_json
from terminal_colors import (
    print_header, print_section, print_success, print_error, 
    print_warning, print_info, print_loading, colored, 
    create_border_box
)

def get_date_range(days):
    """Calculate the date range based on the number of days."""
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    return start_date.strftime('%Y-%m-%dT%H:%M:%SZ'), end_date.strftime('%Y-%m-%dT%H:%M:%SZ')

def batch_search_videos(search_terms, days=7, max_results=10, export_format='json'):
    """
    Perform batch search for multiple search terms.
    
    Args:
        search_terms (list): List of search terms
        days (int): Number of days to look back
        max_results (int): Maximum results per search
        export_format (str): Export format ('json' or 'csv')
    
    Returns:
        dict: Results for each search term
    """
    print_section(f"Batch Processing: Searching for {colored(len(search_terms), 'bright_yellow')} terms")
    
    start_date, end_date = get_date_range(days)
    all_results = {}
    
    for i, term in enumerate(search_terms, 1):
        progress = f"[{colored(i, 'bright_cyan')}/{colored(len(search_terms), 'bright_cyan')}]"
        print_loading(f"{progress} Searching for: \"{colored(term, 'bright_white')}\" in the last {colored(days, 'bright_yellow')} days...")
        
        results = search_top_videos(
            query=term,
            published_after=start_date,
            published_before=end_date,
            max_results=max_results
        )
        
        all_results[term] = results
        
        if results:
            print_success(f"Found {colored(len(results), 'bright_green')} videos.")
            
            # Export individual search results
            filename = f"batch_{term.replace(' ', '_')}"
            filepath = ""
            if export_format == 'json':
                filepath = export_to_json(results, filename=f"{filename}.json", data_type="videos")
            else:
                filepath = export_to_csv(results, filename=f"{filename}.csv", data_type="videos")
            
            print_info(f"Exported to: {colored(filepath, 'bright_cyan')}")
        else:
            print_warning("No videos found.")
        
        # Add a small delay between API calls to avoid rate limiting
        if i < len(search_terms):
            time.sleep(1)
    
    return all_results

def batch_find_competitors(niche_keywords, days=30, max_results=5, export_format='json'):
    """
    Perform batch competitor analysis for multiple niche keywords.
    
    Args:
        niche_keywords (list): List of niche keywords
        days (int): Number of days to look back
        max_results (int): Maximum results per search
        export_format (str): Export format ('json' or 'csv')
    
    Returns:
        dict: Results for each niche keyword
    """
    print_section(f"Batch Processing: Finding competitors for {colored(len(niche_keywords), 'bright_yellow')} niches")
    
    start_date, end_date = get_date_range(days)
    all_results = {}
    
    for i, keyword in enumerate(niche_keywords, 1):
        progress = f"[{colored(i, 'bright_cyan')}/{colored(len(niche_keywords), 'bright_cyan')}]"
        print_loading(f"{progress} Finding competitors for: \"{colored(keyword, 'bright_white')}\" active in the last {colored(days, 'bright_yellow')} days...")
        
        competitors = find_competitors(
            niche_keyword=keyword,
            published_after=start_date,
            published_before=end_date,
            max_results=max_results
        )
        
        all_results[keyword] = competitors
        
        if competitors:
            print_success(f"Found {colored(len(competitors), 'bright_green')} competitors.")
            
            # Export individual competitor results
            filename = f"batch_competitors_{keyword.replace(' ', '_')}"
            filepath = ""
            if export_format == 'json':
                filepath = export_to_json(competitors, filename=f"{filename}.json", data_type="competitors")
            else:
                filepath = export_to_csv(competitors, filename=f"{filename}.csv", data_type="competitors")
            
            print_info(f"Exported to: {colored(filepath, 'bright_cyan')}")
        else:
            print_warning("No competitors found.")
        
        # Add a small delay between API calls to avoid rate limiting
        if i < len(niche_keywords):
            time.sleep(1)
    
    return all_results

def export_summary(all_results, filename, data_type):
    """
    Export a summary of all batch processing results.
    
    Args:
        all_results (dict): Results for each search term or niche keyword
        filename (str): Output filename
        data_type (str): Type of data ('videos' or 'competitors')
    """
    print_loading(f"Generating summary report for {colored(len(all_results), 'bright_yellow')} {data_type} queries...")
    summary = {
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'data_type': data_type,
        'total_queries': len(all_results),
        'results': {}
    }
    
    for term, results in all_results.items():
        summary['results'][term] = {
            'count': len(results),
            'items': results
        }
    
    with open(f"exports/batch_summary_{filename}.json", 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2)
    
    filepath = f"exports/batch_summary_{filename}.json"
    print_success(f"Batch summary exported to: {colored(filepath, 'bright_cyan')}")

def main():
    """Run batch processing examples."""
    print_header("YouTube Automation Tool - Batch Processing", width=70, color='bright_green')
    
    # Example 1: Batch search for videos
    search_terms = [
        "python tutorial",
        "javascript tutorial",
        "data science",
        "machine learning",
        "web development"
    ]
    
    # Display search terms
    print_section("Search Terms")
    for i, term in enumerate(search_terms, 1):
        print(f" {colored(i, 'bright_cyan')}. {colored(term, 'white')}")
    
    video_results = batch_search_videos(
        search_terms=search_terms,
        days=7,
        max_results=5,
        export_format='json'
    )
    
    export_summary(video_results, "video_searches", "videos")
    
    # Example 2: Batch find competitors
    niche_keywords = [
        "data science",
        "web development",
        "digital marketing"
    ]
    
    # Display niche keywords
    print_section("Niche Keywords")
    for i, keyword in enumerate(niche_keywords, 1):
        print(f" {colored(i, 'bright_cyan')}. {colored(keyword, 'white')}")
    
    competitor_results = batch_find_competitors(
        niche_keywords=niche_keywords,
        days=30,
        max_results=3,
        export_format='json'
    )
    
    export_summary(competitor_results, "competitor_searches", "competitors")
    
    print_success("Batch processing completed. Check the exports directory for all results.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print_error("Operation cancelled by user.")
        sys.exit(0)
    except Exception as e:
        print_error(f"An error occurred: {e}")
        sys.exit(1)
