"""
Boot Sequence Module
------------------
Provides a fancy boot sequence for the YouTube Automation Tool.
"""
import time
import sys
import random
import os

# ANSI color codes for customization
COLORS = {
    'red': "\033[31m",
    'green': "\033[32m",
    'yellow': "\033[33m",
    'blue': "\033[34m",
    'magenta': "\033[35m",
    'cyan': "\033[36m",
    'white': "\033[37m",
    'reset': "\033[0m"
}

# Default color for the ASCII logo
DEFAULT_LOGO_COLOR = 'red'

def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def typewriter_effect(text, delay=0.03):
    """Display text with a typewriter effect."""
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def loading_bar(length=40, duration=3):
    """Display a loading bar animation."""
    print("\nInitializing YouTube Automation Tool...")
    print("[", end="")
    for i in range(length):
        time.sleep(duration / length)
        print("█", end="", flush=True)
    print("] 100%")
    print()

def display_ascii_logo(color=DEFAULT_LOGO_COLOR):
    """
    Display ASCII art logo in the specified color.
    
    Args:
        color (str): Color name from the COLORS dictionary
    """
    # Get the color code, default to red if not found
    color_code = COLORS.get(color.lower(), COLORS['red'])
    reset_code = COLORS['reset']
    
    # Placeholder ASCII art - user can replace this with their own design
    logo = r"""
 
▄██   ▄    ▄██████▄  ███    █▄      ███     ███    █▄  ▀█████████▄     ▄████████ 
███   ██▄ ███    ███ ███    ███ ▀█████████▄ ███    ███   ███    ███   ███    ███ 
███▄▄▄███ ███    ███ ███    ███    ▀███▀▀██ ███    ███   ███    ███   ███    █▀  
▀▀▀▀▀▀███ ███    ███ ███    ███     ███   ▀ ███    ███  ▄███▄▄▄██▀   ▄███▄▄▄     
▄██   ███ ███    ███ ███    ███     ███     ███    ███ ▀▀███▀▀▀██▄  ▀▀███▀▀▀     
███   ███ ███    ███ ███    ███     ███     ███    ███   ███    ██▄   ███    █▄  
███   ███ ███    ███ ███    ███     ███     ███    ███   ███    ███   ███    ███ 
 ▀█████▀   ▀██████▀  ████████▀     ▄████▀   ████████▀  ▄█████████▀    ██████████                                                                                       

    ___         __                        __  _           
   /   | __  __/ /_____  ____ ___  ____ _/ /_(_)___  ____ 
  / /| |/ / / / __/ __ \/ __ `__ \/ __ `/ __/ / __ \/ __ \
 / ___ / /_/ / /_/ /_/ / / / / / / /_/ / /_/ / /_/ / / / /
/_/  |_\__,_/\__/\____/_/ /_/ /_/\__,_/\__/_/\____/_/ /_/ 
                                                          
    """
    # Print the logo in the specified color
    print(f"{color_code}{logo}{reset_code}")

def simulate_system_boot():
    """Simulate a system boot with technical-looking messages."""
    boot_messages = [
        "Initializing YouTube API connection..."
    ]
    for message in boot_messages:
        typewriter_effect(message)
        time.sleep(random.uniform(0.3, 0.7))
        print(f"[OK]")
    
    print("\nAll systems operational!\n")
    time.sleep(1)

def run_boot_sequence(logo_color=DEFAULT_LOGO_COLOR):
    """
    Run the complete boot sequence.
    
    Args:
        logo_color (str): Color for the ASCII logo
    """
    clear_screen()
    display_ascii_logo(logo_color)  # First display of the logo
    time.sleep(1)
    loading_bar()
    simulate_system_boot()
    time.sleep(0.5)
    clear_screen()
    display_ascii_logo(logo_color)  # Second display of the logo
    print("\nYouTube Automation Tool v1.0")
    print("======================\n")
    time.sleep(1)

if __name__ == "__main__":
    # Test the boot sequence if this file is run directly
    # You can change the color here for testing
    run_boot_sequence(DEFAULT_LOGO_COLOR)
