#!/usr/bin/env python3
# This line above is called a "shebang" - it tells the computer which program to use to run this file
# In this case, it's saying "use Python 3 to run this file"

"""
YouTube Automation Tool
-----------------------
A CLI tool to search for top YouTube videos or find competitors in a niche.
"""
# The text above in triple quotes is called a "docstring" - it's a description of what this program does
# CLI means "Command Line Interface" - a way to run programs by typing commands instead of clicking buttons
# IMPORTS SECTION
# "import" means we're bringing in code from other files to use in this program
# Think of it like borrowing tools from different toolboxes to help us build something

import sys                  # This gives us tools to interact with the computer system
import time                 # This gives us tools to work with time (like pausing the program)
import argparse             # This helps us handle command-line arguments (options typed when starting the program)
from datetime import datetime, timedelta  # Tools for working with dates and times
from youtube_api import YouTubeAPI        # Our custom code for talking to YouTube
from search_utils import search_top_videos  # Our custom code for searching videos
from competitor_utils import find_competitors  # Our custom code for finding competitors
from export_utils import export_to_csv, export_to_json  # Our custom code for saving results to files
from boot_sequence import run_boot_sequence  # Our custom code for the startup animation
from terminal_colors import (  # Our custom code for making colorful text in the terminal
    print_header, print_section, print_option, print_result_item,
    print_success, print_error, print_info, print_warning, print_loading,
    create_border_box, input_colored, colored, print_query_box
)

# FUNCTIONS SECTION
# "def" means we're defining a function - a reusable block of code that does a specific task
# Functions are like mini-programs within our main program
# They help us organize our code and avoid repeating ourselves

def get_user_export_choice():
    """Ask the user if they want to export results and in what format."""
    # This triple-quoted text is a "docstring" that explains what this function does
    # This function shows export options to the user and gets their choice
    
    # Display a box with numbered options
    print_query_box("Export Options", [
        "Export to CSV",      # CSV is a simple file format that can be opened in Excel
        "Export to JSON",     # JSON is a file format used by many programs and websites
        "No export"           # Option to not save the results
    ])
    
    # This is a loop - it keeps running the code inside until we break out of it
    while True:
        # Ask the user to type their choice and store it in the variable "choice"
        choice = input_colored("Enter your choice (1-3)")
        # Check if they entered a valid option
        if choice in ["1", "2", "3"]:
            return choice  # "return" sends this value back to wherever this function was called from
        # If we get here, the user didn't enter 1, 2, or 3, so show an error
        print_error("Invalid choice. Please enter a number between 1 and 3.")

def export_results(data, data_type):
    """Export results based on user choice."""
    # This function saves the search results to a file
    # "data" contains the results we want to save
    # "data_type" tells us if we're saving videos or competitors
    
    # Call the function we defined above to ask the user how they want to export
    choice = get_user_export_choice()
    
    # If they chose option 3 (No export), exit the function without doing anything
    if choice == "3":
        return  # "return" with no value just exits the function
    
    # Show a loading message while we export the data
    # The f"..." syntax is an f-string - it lets us put variables inside text
    print_loading(f"Exporting {data_type} data...")
    
    # Handle the different export choices
    if choice == "1":
        # Export to CSV file
        filepath = export_to_csv(data, data_type=data_type)
        # Show a success message with the file path in cyan color
        print_success(f"Data exported successfully to {colored(filepath, 'bright_cyan')}")
    elif choice == "2":
        # Export to JSON file
        filepath = export_to_json(data, data_type=data_type)
        # Show a success message with the file path in cyan color
        print_success(f"Data exported successfully to {colored(filepath, 'bright_cyan')}")

def get_date_range(days):
    """Calculate the date range based on the number of days."""
    # This function calculates a date range from today going back a certain number of days
    # For example, if days=7, it gives us the date range for the last week
    
    # Get the current date and time
    end_date = datetime.now()
    # Calculate the start date by subtracting the number of days
    start_date = end_date - timedelta(days=days)
    
    # Convert the dates to a specific text format that YouTube's API requires
    # The format is: YYYY-MM-DDThh:mm:ssZ (Year-Month-DayTHour:Minute:SecondZ)
    # The 'T' separates the date and time, and 'Z' means UTC timezone
    return start_date.strftime('%Y-%m-%dT%H:%M:%SZ'), end_date.strftime('%Y-%m-%dT%H:%M:%SZ')

def parse_arguments():
    """Parse command-line arguments."""
    # This function handles options that users can type when starting the program
    # For example: python main.py --no-boot
    
    # Create a parser object that will understand the command-line arguments
    parser = argparse.ArgumentParser(description='YouTube Automation Tool')
    
    # Add the --no-boot option
    # When this option is used, it will skip the startup animation
    parser.add_argument('--no-boot', action='store_true', 
                        help='Skip the boot sequence animation')
    
    # Add the --quick-search option
    # This lets users do a quick search without going through the interactive menu
    # Example: python main.py --quick-search "cooking recipes"
    parser.add_argument('--quick-search', type=str, metavar='QUERY',
                        help='Quickly search for videos with the given query (uses default settings)')
    
    # Process the arguments and return them
    return parser.parse_args()

def main():
    """Main function to run the YouTube automation tool."""
    # This is the main function that runs when you start the program
    # It controls the overall flow of the program
    # Parse command-line arguments (options typed when starting the program)
    args = parse_arguments()
    
    # Run the fancy boot sequence (startup animation) unless --no-boot is specified
    if not args.no_boot:
        # Show the animated startup sequence with a red color theme
        run_boot_sequence('red')  # Explicitly set the logo color to red
    else:
        # If --no-boot was specified, just show a simple header instead
        print_header("YouTube Automation Tool", width=60, color='bright_red')
    
    # QUICK SEARCH SECTION
    # Check if the user specified a quick search when starting the program
    if args.quick_search:
        # Show a loading message with the search term
        print_loading(f"Quick search for: \"{args.quick_search}\" in the last 7 days...")
        
        # Get the date range for the last 7 days
        start_date, end_date = get_date_range(7)
        
        # Search for videos using the search term and date range
        results = search_top_videos(args.quick_search, start_date, end_date)
        
        # If we found any videos
        if results:
            # Show a section header with the number of results
            print_section(f"Top Videos Found: {colored(len(results), 'bright_green')} results")
            
            # Loop through each video in the results
            # enumerate(results, 1) gives us both the index (starting at 1) and the video
            for i, video in enumerate(results, 1):
                # Convert published date to human-readable format (dd/mm/yyyy)
                published_date = video['published_at'].split('T')[0]  # Extract YYYY-MM-DD
                date_parts = published_date.split('-')
                if len(date_parts) == 3:
                    published_date = f"{date_parts[2]}/{date_parts[1]}/{date_parts[0]}"  # DD/MM/YYYY
                
                # Calculate performance metric (Likes / Views) * 100 - percentage of viewers who liked
                # If view_count is 0, use 1 instead to avoid division by zero error
                views = video['view_count'] if video['view_count'] > 0 else 1
                performance_score = (video['like_count'] / views) * 100
                
                # Determine performance message and color based on score
                if performance_score >= 5:  # 5% or more likes-to-views is excellent engagement
                    performance_msg = colored("MAKE THIS VIDEO NOW", 'bright_green', style='bold')
                elif performance_score >= 2:  # 2-5% likes-to-views is good engagement
                    performance_msg = colored("Great", 'bright_blue')
                else:  # Less than 2% likes-to-views is lower engagement
                    performance_msg = colored("Not the best", 'yellow')
                
                # Create a dictionary with all the details we want to show
                details = {
                    "Channel": video['channel_title'],
                    "Views": f"{video['view_count']:,}",  # The :, adds commas to large numbers
                    "Likes": f"{video['like_count']:,}",
                    "Published": published_date,
                    "URL": f"https://www.youtube.com/watch?v={video['video_id']}",
                    "Performance": f"Score: {performance_score:.2f} - {performance_msg}"  # .2f means 2 decimal places
                }
                
                # Print the video title and details
                print_result_item(i, video['title'], details)
            
            # Offer to export results to a file
            export_results(results, 'videos')
        else:
            # If no videos were found, show a warning
            print_warning("No videos found matching your criteria.")
        
        # Exit the program with status code 0 (meaning success)
        # sys.exit() stops the program immediately
        sys.exit(0)
    
    # MAIN MENU SECTION
    # If we get here, the user didn't use --quick-search, so show the interactive menu
    
    # Display the main menu options
    print_query_box("Main Menu", [
        "Search for top videos",
        "Find best competitors"
    ])
    
    # Keep asking until we get a valid choice
    while True:
        choice = input_colored("Respond with either \"1\" or \"2\"")
        if choice in ["1", "2"]:
            break  # Exit the loop if they entered 1 or 2
        print_error("Invalid choice. Please enter either \"1\" or \"2\".")
    
    # OPTION 1: SEARCH FOR TOP VIDEOS
    if choice == "1":
        # Show a section header for video search
        print_section("Video Search")
        print_info(" Place ONLY your search term and send when you're ready")
        
        # Ask for the search term
        search_term = input_colored("Search term")
        
        # Ask for the time range
        print_query_box("Time Range", [
            "Last 7 days",
            "Last 30 days"
        ])
        
        # Keep asking until we get a valid choice
        while True:
            time_range = input_colored("Select time range (1-2)")
            if time_range in ["1", "2"]:
                break  # Exit the loop if they entered 1 or 2
            print_error("Invalid choice. Please enter either \"1\" or \"2\".")
        
        # Convert their choice to a number of days
        # This is a conditional expression: if time_range is "1", days = 7, otherwise days = 30
        days = 7 if time_range == "1" else 30
        
        # Get the date range based on the number of days
        start_date, end_date = get_date_range(days)
        
        # Create a nicely formatted summary of what we're searching for
        search_info = f"""
Searching for: "{colored(search_term, 'bright_yellow')}"
Time range: Last {colored(days, 'bright_yellow')} days
Date range: {colored(start_date.split('T')[0], 'bright_cyan')} to {colored(end_date.split('T')[0], 'bright_cyan')}
"""
        # Display the search info in a colored border box
        print(create_border_box(search_info, width=70, color='bright_magenta'))
        
        # Show a loading message while we search
        print_loading(f"Searching for: \"{colored(search_term, 'bright_yellow')}\" in the last {days} days...")
        
        # Call the search_top_videos function to get the results
        results = search_top_videos(search_term, start_date, end_date)
        
        # Display the results
        if results:
            # Create a header showing how many results we found
            results_header = f"Top Videos Found: {colored(len(results), 'bright_green')} results"
            print_header(results_header, width=70, color='bright_green')
            
            # Loop through each video in the results
            for i, video in enumerate(results, 1):
                # Convert published date to human-readable format (dd/mm/yyyy)
                published_date = video['published_at'].split('T')[0]  # Extract YYYY-MM-DD
                date_parts = published_date.split('-')
                if len(date_parts) == 3:
                    published_date = f"{date_parts[2]}/{date_parts[1]}/{date_parts[0]}"  # DD/MM/YYYY
                
                # Calculate performance metric (Likes / Views) * 100 - percentage of viewers who liked
                views = video['view_count'] if video['view_count'] > 0 else 1  # Avoid division by zero
                performance_score = (video['like_count'] / views) * 100
                
                # Determine performance message and color based on score
                if performance_score >= 5:  # 5% or more likes-to-views is excellent engagement
                    performance_msg = colored("MAKE THIS VIDEO NOW", 'bright_green', style='bold')
                elif performance_score >= 2:  # 2-5% likes-to-views is good engagement
                    performance_msg = colored("Great", 'bright_blue')
                else:  # Less than 2% likes-to-views is lower engagement
                    performance_msg = colored("Not the best", 'yellow')
                
                # Create a dictionary with all the details we want to show
                details = {
                    "Channel": video['channel_title'],
                    "Views": f"{video['view_count']:,}",
                    "Likes": f"{video['like_count']:,}",
                    "Published": published_date,
                    "URL": f"https://www.youtube.com/watch?v={video['video_id']}",
                    "Performance": f"Score: {performance_score:.2f} - {performance_msg}"
                }
                
                # Print the video title and details
                print_result_item(i, video['title'], details)
            
            # Offer to export results to a file
            export_results(results, 'videos')
        else:
            # If no videos were found, show a warning
            print_warning("No videos found matching your criteria.")
            
    # OPTION 2: FIND BEST COMPETITORS
    elif choice == "2":
        # Show a section header for competitor analysis
        print_section("Competitor Analysis")
        print_info(" Place ONLY your niche keyword and send when you're ready")
        
        # Ask for the niche keyword
        niche_keyword = input_colored("Niche keyword")
        
        # Ask for the time range
        print_query_box("Time Range", [
            "Last 7 days",
            "Last 30 days"
        ])
        
        # Keep asking until we get a valid choice
        while True:
            time_range = input_colored("Select time range (1-2)")
            if time_range in ["1", "2"]:
                break  # Exit the loop if they entered 1 or 2
            print_error("Invalid choice. Please enter either \"1\" or \"2\".")
        
        # Convert their choice to a number of days
        days = 7 if time_range == "1" else 30
        
        # Get the date range based on the number of days
        start_date, end_date = get_date_range(days)
        
        # Create a nicely formatted summary of what we're searching for
        search_info = f"""
Finding competitors for: "{colored(niche_keyword, 'bright_yellow')}"
Time range: Last {colored(days, 'bright_yellow')} days
Date range: {colored(start_date.split('T')[0], 'bright_cyan')} to {colored(end_date.split('T')[0], 'bright_cyan')}
"""
        # Display the search info in a colored border box
        print(create_border_box(search_info, width=70, color='bright_blue'))
        
        # Show a loading message while we search
        print_loading(f"Finding competitors for: \"{colored(niche_keyword, 'bright_yellow')}\" active in the last {days} days...")
        
        # Call the find_competitors function to get the results
        competitors = find_competitors(niche_keyword, start_date, end_date)
        
        # Display the results
        if competitors:
            # Create a header showing how many competitors we found
            results_header = f"Top Competitors Found: {colored(len(competitors), 'bright_green')} results"
            print_header(results_header, width=70, color='bright_green')
            
            # Loop through each competitor in the results
            for i, competitor in enumerate(competitors, 1):
                # Create a dictionary with all the details we want to show
                details = {
                    "Subscribers": f"{competitor['subscriber_count']:,}",  # The :, adds commas to large numbers
                    "Total Videos": competitor['video_count'],
                    "Total Views": f"{competitor['view_count']:,}",
                    "Channel URL": f"https://www.youtube.com/channel/{competitor['channel_id']}"
                }
                # Print the competitor name and details
                print_result_item(i, competitor['channel_title'], details)
            
            # Offer to export results to a file
            export_results(competitors, 'competitors')
        else:
            # If no competitors were found, show a warning
            print_warning("No competitors found matching your criteria.")

# This special if statement checks if this file is being run directly (not imported by another file)
# It's a common Python pattern to ensure code only runs when the file is executed directly
if __name__ == "__main__":
    # The try/except blocks below are for error handling
    # They catch errors that might happen while the program is running
    try:
        # Call the main function to start the program
        main()
    except KeyboardInterrupt:
        # This catches when the user presses Ctrl+C to stop the program
        print_error("Operation cancelled by user.")
        sys.exit(0)  # Exit with status code 0 (success)
    except Exception as e:
        # This catches any other errors that might happen
        print_error(f"An error occurred: {e}")
        sys.exit(1)  # Exit with status code 1 (error)
