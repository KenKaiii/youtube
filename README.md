# YouTube Automation Tool

A command-line tool to search for top YouTube videos or find competitors in your niche.

## Features

- Search for top videos based on a keyword and time range (last 7 or 30 days)
- Find the best competitors in your niche
- Sort results by view count, engagement, and relevance
- Performance metrics to identify high-potential video topics
- Human-readable date formats for better readability
- Export results to CSV or JSON files for further analysis
- Test script to verify API connection and functionality

## Setup

Clone the repository
1. Create a folder where you want it to go (eg. YouTube folder)
2. Navigate to that folder in Powershell (cd YouTube)
3. Git clone the repo:
```
git clone https://github.com/KenKaiii/youtube
```

### Automatic Setup (Recommended)

#### On Linux/macOS:
```
chmod +x setup.sh
./setup.sh
```

#### On Windows:
```
.\setup.bat
```

The setup script will:
1. Create a virtual environment
2. Install required dependencies
3. Create the exports directory
4. Prompt you for your YouTube API key and create a .env file

### Manual Setup

If you prefer to set up manually:

1. Clone this repository
2. Create and activate a virtual environment (optional but recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Linux/macOS
   venv\Scripts\activate.bat  # On Windows
   ```
3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Get a YouTube Data API key:
   - Go to the [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project
   - Enable the YouTube Data API v3
   - Create an API key
   - Copy the API key

5. Create a `.env` file in the project root directory with your API key:
   ```
   YOUTUBE_API_KEY=your_api_key_here
   ```
   (You can use the provided `.env.example` file as a template)
6. Create an `exports` directory for storing exported data:
   ```
   mkdir exports
   ```

## Usage

### Main Tool

Activate the virtual environment

```
venv\Scripts\activate
```
Run the main tool using Python:

```
python main.py
```

The tool will display a fancy boot sequence animation and then prompt you for input.

### Command-line Arguments

The tool supports several command-line arguments:

```
python main.py --no-boot                # Skip the boot sequence animation
python main.py --quick-search "python"  # Quickly search for videos with the given query
```

For a full list of options:

```
python main.py --help
```

### Using as a Module

You can also use the YouTube Automation Tool as a module in your own Python scripts. Check out the example scripts:

```
python example_usage.py    # Basic usage examples
python batch_processing.py # Batch processing multiple searches
```

These demonstrate how to:
- Search for videos programmatically
- Find competitors programmatically
- Analyze a specific competitor
- Export results to files
- Process multiple search terms in batch
- Generate summary reports

### Testing API Connection

Before using the main tool, you can verify your API connection:

```
python test_api.py
```

This will test if your API key is valid and if the YouTube API is accessible.

Follow the prompts to:
1. Choose between searching for top videos or finding competitors
2. Enter your search term or niche keyword
3. Select the time range (last 7 days or last 30 days)

### Example: Searching for Top Videos

```
YouTube Automation Tool
======================

Would you like to search for top videos, or find the best competitors in your niche?
1. Search for top videos
2. Find best competitors
Respond with either "1" or "2": 1

Place ONLY your search term and send when you're ready
Search term: python tutorial

Would you like videos in the last 7 days or last 30 days?
Type "1" for 7 days or "2" for 30 days: 1

Searching for: "python tutorial" in the last 7 days...

Top Videos Found:
...

Would you like to export the results?
1. Export to CSV
2. Export to JSON
3. No export
Enter your choice (1-3): 1

Data exported successfully to exports/videos_20250411_145520.csv
```

### Example: Finding Competitors

```
YouTube Automation Tool
======================

Would you like to search for top videos, or find the best competitors in your niche?
1. Search for top videos
2. Find best competitors
Respond with either "1" or "2": 2

Place ONLY your niche keyword and send when you're ready
Niche keyword: data science

Would you like to analyze channels active in the last 7 days or last 30 days?
Type "1" for 7 days or "2" for 30 days: 2

Finding competitors for: "data science" active in the last 30 days...

Top Competitors Found:
...

Would you like to export the results?
1. Export to CSV
2. Export to JSON
3. No export
Enter your choice (1-3): 2

Data exported successfully to exports/competitors_20250411_145520.json
```

## Customization

You can customize the tool by modifying the following files:

- `config.py`: Change API settings and default parameters
- `youtube_api.py`: Modify API interaction logic
- `search_utils.py`: Customize search functionality
- `competitor_utils.py`: Adjust competitor analysis algorithms
- `export_utils.py`: Modify export functionality and formats
- `boot_sequence.py`: Customize the boot animation and ASCII art
  - The ASCII logo color can be changed by modifying the `DEFAULT_LOGO_COLOR` constant
  - Available colors: red, green, yellow, blue, magenta, cyan, white
- `terminal_colors.py`: Utility functions for colored terminal output
  - Provides functions for colored text, headers, sections, and borders
  - Makes the CLI interface more visually appealing and easier to read
  - Optimized for black background terminals like PowerShell
  - Features bordered query boxes and highlighted interactive elements

## Exported Data

When you choose to export data, files are saved in the `exports` directory with the following naming convention:

- CSV files: `[data_type]_[timestamp].csv` (e.g., `videos_20250411_145520.csv`)
- JSON files: `[data_type]_[timestamp].json` (e.g., `competitors_20250411_145520.json`)

### Video Data Fields

The exported video data includes:

- **Basic Information**: video_id, title, channel_title
- **Date Information**: published_date (DD/MM/YYYY), published_at (ISO format)
- **Statistics**: view_count, like_count, comment_count
- **Performance Metrics**: 
  - performance_score: (Likes / Views) × 100 (percentage of viewers who liked the video)
  - performance_rating: "MAKE THIS VIDEO NOW" (score ≥ 5%), "Great" (score 2-5%), or "Not the best" (score < 2%)

### Competitor Data Fields

The exported competitor data includes:

- **Basic Information**: channel_id, channel_title
- **Statistics**: subscriber_count, video_count, view_count
- **Analysis**: engagement_score, relevance_score

## Limitations

- The YouTube Data API has daily quota limits (10,000 units per day for free tier)
- Results are limited to what's available through the YouTube API
- The tool requires an internet connection to function

## Search Parameters

The tool uses the following parameters for YouTube searches:

- **Region**: US (regionCode='US')
- **Language**: English (relevanceLanguage='en')
- **Order**: By view count (order='viewCount')
- **Type**: Videos only (type='video')
- **Max Results**: 50 by default (configurable in config.py)

These parameters can be customized in the youtube_api.py file if needed.

## License

This project is open source and available under the MIT License.
