# Setup Instructions

## Setting up the Virtual Environment

This project uses a virtual environment to manage dependencies. Follow these steps to set it up:

### Windows

```
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Linux/macOS

```
# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Setting up the API Key

This project requires a YouTube Data API key to function. The API key is stored in a `.env` file to keep it secure and separate from the code.

### Using the Setup Scripts (Recommended)

The easiest way to set up your API key is to use the provided setup scripts:

#### Windows
```
setup.bat
```

#### Linux/macOS
```
chmod +x setup.sh
./setup.sh
```

These scripts will prompt you for your API key and create the `.env` file automatically.

### Manual Setup

If you prefer to set up the API key manually:

1. Copy the `.env.example` file to a new file named `.env`:
   ```
   cp .env.example .env  # Linux/macOS
   copy .env.example .env  # Windows
   ```

2. Edit the `.env` file and replace `your_api_key_here` with your actual YouTube API key:
   ```
   YOUTUBE_API_KEY=your_actual_api_key_here
   ```

## Troubleshooting Import Issues

If you're seeing import errors for `googleapiclient` or other packages, make sure:

1. You've activated the virtual environment (you should see `(venv)` at the beginning of your command prompt)
2. You've installed all dependencies with `pip install -r requirements.txt`

### Common Import Errors

#### Error: No module named 'googleapiclient'

This means the Google API Client Library hasn't been installed. Run:

```
pip install google-api-python-client
```

#### Error: No module named 'google.auth'

This means the Google Auth Library hasn't been installed. Run:

```
pip install google-auth google-auth-httplib2 google-auth-oauthlib
```

## Running the Application

Always make sure the virtual environment is activated before running any scripts:

```
# Windows
venv\Scripts\activate

# Linux/macOS
source venv/bin/activate
```

Then you can run the application:

```
python main.py
```

### Boot Sequence

The application includes a fancy boot sequence with animations. If you prefer to skip this:

```
python main.py --no-boot
```

### Quick Search

For a quick search without going through all the prompts:

```
python main.py --quick-search "your search term"
```

### Testing the API Connection

To test your API connection before using the main application:

```
python test_api.py
```

### Running the Boot Sequence Separately

You can also run just the boot sequence animation to test it:

```
python boot_sequence.py
```

### Customizing the Interface

#### Boot Sequence

The boot sequence can be customized by editing the `boot_sequence.py` file:

##### Changing the ASCII Logo Color

The ASCII logo is displayed in red by default. You can change this by modifying the `DEFAULT_LOGO_COLOR` constant at the top of the file:

```python
# Default color for the ASCII logo
DEFAULT_LOGO_COLOR = 'red'  # Change to 'green', 'blue', 'yellow', etc.
```

Available colors:
- red
- green
- yellow
- blue
- magenta
- cyan
- white

#### Terminal Colors

The terminal output colors are optimized for black background terminals like PowerShell. They can be customized by editing the `terminal_colors.py` file. This module provides utility functions for colored text and formatting:

```python
# Examples of using terminal_colors functions
from terminal_colors import colored, print_colored, print_header, print_query_box

# Colored text
colored_text = colored("Hello, World!", "bright_green", style="bold")
print(colored_text)

# Print colored text directly
print_colored("Warning message", "bright_yellow")

# Print a header with borders
print_header("Section Title", color="bright_cyan")

# Print a query box with options
print_query_box("Select an Option", [
    "Option One",
    "Option Two",
    "Option Three"
])
```

##### Color Scheme

The colors are optimized for black background terminals with high contrast:

```python
# Default colors for different types of output
DEFAULT_COLORS = {
    'header': 'bright_cyan',
    'section': 'bright_yellow',
    'option_number': 'bright_cyan',
    'option_text': 'bright_white',
    'result_number': 'bright_green',
    'result_title': 'bright_white',
    'result_details_key': 'bright_cyan',
    'result_details_value': 'bright_white',
    'success': 'bright_green',
    'error': 'bright_red',
    'warning': 'bright_yellow',
    'info': 'bright_blue',
    'loading': 'bright_magenta',
    'border': 'bright_cyan',
    'highlight': 'bright_yellow',
    'prompt': 'bright_green',
}
```

You can modify these colors to suit your preferences or terminal background.

##### Available Functions

- `colored(text, color, bg_color, style)`: Return colored text
- `print_colored(text, color, bg_color, style)`: Print colored text
- `print_header(text, width, color, style)`: Print a header with double-line borders
- `print_section(text, color, style)`: Print a section title with single-line borders
- `print_option(number, text, color_num, color_text)`: Print a numbered option with arrow
- `print_result_item(number, title, details)`: Print a result item with details in a bordered box
- `print_success(text)`: Print a success message in a green bordered box
- `print_error(text)`: Print an error message in a red bordered box
- `print_warning(text)`: Print a warning message in a yellow bordered box
- `print_info(text)`: Print an info message in a blue bordered box
- `print_loading(text)`: Print a loading message in a magenta bordered box
- `create_border_box(text, width, color)`: Create a border box around text
- `input_colored(prompt, color, style)`: Get input with a colored prompt in a bordered box
- `print_query_box(title, options, color)`: Print a query box with title and options

### Advanced Usage Examples

#### Example Script

To see examples of how to use the tool programmatically:

```
python example_usage.py
```

#### Batch Processing

For processing multiple search terms or competitor analyses in one run:

```
python batch_processing.py
```

This script demonstrates:
- How to search for multiple terms in batch
- How to find competitors for multiple niches
- How to export individual results and summary reports

### Performance Metrics

The tool now includes a performance metric for videos that helps identify high-potential topics:

- **Performance Score**: Calculated as (Likes / Views) × 100 (percentage of viewers who liked the video)
- **Performance Rating**:
  - "MAKE THIS VIDEO NOW" (green): Score ≥ 5% (high engagement)
  - "Great" (blue): Score between 2-5% (good engagement)
  - "Not the best" (orange): Score < 2% (lower engagement)

This metric helps identify topics where viewers are highly engaged relative to the view count, suggesting content that resonates well with the audience.

### Date Formatting

Dates are now displayed in a human-readable format:

- **Display Format**: DD/MM/YYYY
- **Export Format**: Both human-readable (published_date) and ISO format (published_at) are included in exports

### Search Parameters

The tool is configured to search for English language videos in the US region. If you're seeing videos in other languages, this is because the YouTube API uses the following parameters:

```python
search_params = {
    'q': query,
    'type': 'video',
    'part': 'id,snippet',
    'maxResults': max_results,
    'regionCode': 'US',
    'relevanceLanguage': 'en',  # Filter for English language videos
    'order': 'viewCount'
}
```

You can modify these parameters in the `youtube_api.py` file if you want to search in a different language or region.
