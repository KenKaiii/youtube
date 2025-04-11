"""
Terminal Colors Module
--------------------
Provides utility functions for colored terminal output.
Optimized for black background terminals like PowerShell.
"""

# ANSI color codes - optimized for black background
COLORS = {
    # Standard colors - avoid dark colors on black background
    'black': '\033[30m',  # Not recommended on black background
    'red': '\033[31m',    # Use bright_red instead for better visibility
    'green': '\033[32m',  # Use bright_green instead for better visibility
    'yellow': '\033[33m', 
    'blue': '\033[34m',   # Use bright_blue instead for better visibility
    'magenta': '\033[35m',
    'cyan': '\033[36m',
    'white': '\033[37m',
    'reset': '\033[0m',
    
    # Bright colors - better visibility on black background
    'bright_black': '\033[90m',  # Not recommended on black background
    'bright_red': '\033[91m',    # Good contrast
    'bright_green': '\033[92m',  # Good contrast
    'bright_yellow': '\033[93m', # Good contrast
    'bright_blue': '\033[94m',   # Good contrast
    'bright_magenta': '\033[95m',# Good contrast
    'bright_cyan': '\033[96m',   # Good contrast
    'bright_white': '\033[97m',  # Good contrast
}

# Default colors for different types of output - optimized for black background
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

# ANSI background color codes
BG_COLORS = {
    'black': '\033[40m',
    'red': '\033[41m',
    'green': '\033[42m',
    'yellow': '\033[43m',
    'blue': '\033[44m',
    'magenta': '\033[45m',
    'cyan': '\033[46m',
    'white': '\033[47m',
}

# ANSI text style codes
STYLES = {
    'bold': '\033[1m',
    'underline': '\033[4m',
    'blink': '\033[5m',
    'reverse': '\033[7m',
}

def colored(text, color=None, bg_color=None, style=None):
    """
    Return text with specified color, background color, and/or style.
    
    Args:
        text (str): The text to color
        color (str): Text color name from COLORS
        bg_color (str): Background color name from BG_COLORS
        style (str): Text style name from STYLES
        
    Returns:
        str: Colored text
    """
    result = ""
    
    if style and style in STYLES:
        result += STYLES[style]
    
    if color and color in COLORS:
        result += COLORS[color]
    
    if bg_color and bg_color in BG_COLORS:
        result += BG_COLORS[bg_color]
    
    result += str(text) + COLORS['reset']
    return result

def print_colored(text, color=None, bg_color=None, style=None):
    """Print colored text."""
    print(colored(text, color, bg_color, style))

def print_header(text, width=60, color=DEFAULT_COLORS['header'], style='bold'):
    """Print a header with borders."""
    # Calculate exact width for content
    content_width = width - 4  # Subtract 4 for the border characters and spaces
    
    # Create the border line with exact width
    border_line = '═' * content_width
    
    # Center the text within the content width
    padded_text = text.center(content_width)
    
    # Print with consistent alignment
    print_colored(f"╔{border_line}╗", color, style=style)
    print_colored(f"║ {padded_text} ║", color, style=style)
    print_colored(f"╚{border_line}╝", color, style=style)

def print_section(text, color=DEFAULT_COLORS['section'], style='bold'):
    """Print a section title."""
    # Calculate content width based on text length
    content_width = len(text) + 8  # Add 8 for padding and arrow
    
    # Create borders with exact width
    border_top = '─' * content_width
    border_bottom = '─' * content_width
    
    # Calculate padding to ensure text is centered
    text_with_arrow = f"▶ {text}"
    left_padding = (content_width - len(text_with_arrow)) // 2
    right_padding = content_width - len(text_with_arrow) - left_padding
    padded_text = ' ' * left_padding + text_with_arrow + ' ' * right_padding
    
    print()
    print_colored(f"┌{border_top}┐", color, style=style)
    print_colored(f"│{padded_text}│", color, style=style)
    print_colored(f"└{border_bottom}┘", color, style=style)

def print_option(number, text, color_num=DEFAULT_COLORS['option_number'], color_text=DEFAULT_COLORS['option_text']):
    """Print a numbered option."""
    print(f" {colored('►', color_num)} {colored(number, color_num, style='bold')}. {colored(text, color_text)}")

def print_result_item(number, title, details, 
                     color_num=DEFAULT_COLORS['result_number'], 
                     color_title=DEFAULT_COLORS['result_title'], 
                     color_details_key=DEFAULT_COLORS['result_details_key'],
                     color_details_value=DEFAULT_COLORS['result_details_value']):
    """Print a result item with number, title and details."""
    # Calculate width based on content
    title_len = len(title)
    number_len = len(str(number))
    
    # Calculate the maximum width needed for details
    max_detail_width = 0
    for key, value in details.items():
        key_str = f"{key}:"
        value_str = f"{value}"
        detail_width = len(key_str) + len(value_str) + 2  # +2 for space between key and value
        max_detail_width = max(max_detail_width, detail_width)
    
    # Set minimum width and ensure it's wide enough for all content
    content_width = max(title_len + number_len + 4, max_detail_width, 60)
    
    # Create borders with exact width
    border_line = '─' * content_width
    
    # Print result with borders
    print()
    print_colored(f"┌{border_line}┐", DEFAULT_COLORS['border'])
    
    # Print title with proper padding
    title_display = f"{colored(number, color_num, style='bold')}. {colored(title, color_title, style='bold')}"
    padding = content_width - (number_len + 2 + title_len)
    print_colored(f"│{title_display}{' ' * padding}│", DEFAULT_COLORS['border'])
    
    print_colored(f"├{border_line}┤", DEFAULT_COLORS['border'])
    
    # Print details with proper padding
    for key, value in details.items():
        key_str = f"{key}:"
        value_str = f"{value}"
        detail_display = f" {colored(key_str, color_details_key)} {colored(value_str, color_details_value)}"
        padding = content_width - (len(key_str) + len(value_str) + 2)
        print_colored(f"│{detail_display}{' ' * padding}│", DEFAULT_COLORS['border'])
    
    print_colored(f"└{border_line}┘", DEFAULT_COLORS['border'])

def print_success(text):
    """Print a success message."""
    message = f"✓ {text}"
    content_width = len(message) + 2  # Add 2 for padding
    border_line = '─' * content_width
    
    print()
    print_colored(f"┌{border_line}┐", DEFAULT_COLORS['success'])
    print_colored(f"│ {message} │", DEFAULT_COLORS['success'], style='bold')
    print_colored(f"└{border_line}┘", DEFAULT_COLORS['success'])

def print_error(text):
    """Print an error message."""
    message = f"✗ {text}"
    content_width = len(message) + 2  # Add 2 for padding
    border_line = '─' * content_width
    
    print()
    print_colored(f"┌{border_line}┐", DEFAULT_COLORS['error'])
    print_colored(f"│ {message} │", DEFAULT_COLORS['error'], style='bold')
    print_colored(f"└{border_line}┘", DEFAULT_COLORS['error'])

def print_info(text):
    """Print an info message."""
    message = f"ℹ {text}"
    content_width = len(message) + 2  # Add 2 for padding
    border_line = '─' * content_width
    
    print()
    print_colored(f"┌{border_line}┐", DEFAULT_COLORS['info'])
    print_colored(f"│ {message} │", DEFAULT_COLORS['info'])
    print_colored(f"└{border_line}┘", DEFAULT_COLORS['info'])

def print_warning(text):
    """Print a warning message."""
    message = f"⚠ {text}"
    content_width = len(message) + 2  # Add 2 for padding
    border_line = '─' * content_width
    
    print()
    print_colored(f"┌{border_line}┐", DEFAULT_COLORS['warning'])
    print_colored(f"│ {message} │", DEFAULT_COLORS['warning'], style='bold')
    print_colored(f"└{border_line}┘", DEFAULT_COLORS['warning'])

def print_loading(text):
    """Print a loading message."""
    # Calculate the visible length of the text (without color codes)
    visible_text = text
    for color_name, color_code in COLORS.items():
        visible_text = visible_text.replace(color_code, '')
    
    message = f"⟳ {text}"
    visible_message = f"⟳ {visible_text}"
    
    # Calculate content width based on visible length
    content_width = len(visible_message) + 2  # Add 2 for padding
    border_line = '─' * content_width
    
    print()
    print_colored(f"┌{border_line}┐", DEFAULT_COLORS['loading'])
    print_colored(f"│ {message} │", DEFAULT_COLORS['loading'])
    print_colored(f"└{border_line}┘", DEFAULT_COLORS['loading'])

def create_border_box(text, width=60, color=DEFAULT_COLORS['border']):
    """Create a border box around text."""
    lines = text.split('\n')
    # Remove empty lines at the beginning and end
    while lines and not lines[0].strip():
        lines.pop(0)
    while lines and not lines[-1].strip():
        lines.pop()
    
    if not lines:
        return ""
    
    # Calculate the maximum visible line length (without color codes)
    max_line_length = 0
    for line in lines:
        visible_line = line
        for color_name, color_code in COLORS.items():
            visible_line = visible_line.replace(color_code, '')
        max_line_length = max(max_line_length, len(visible_line))
    
    # Ensure minimum width and add padding
    content_width = max(width - 4, max_line_length)
    
    # Create borders with exact width
    border_line = '═' * content_width
    
    result = colored(f"╔{border_line}╗", color) + '\n'
    
    for line in lines:
        # Calculate the visible length of the line (without color codes)
        visible_line = line
        for color_name, color_code in COLORS.items():
            visible_line = visible_line.replace(color_code, '')
        
        # Calculate padding to ensure the line fills the box width
        padding = content_width - len(visible_line)
        result += colored("║ ", color) + line + " " * padding + colored(" ║", color) + '\n'
    
    result += colored(f"╚{border_line}╝", color)
    return result

def input_colored(prompt, color=DEFAULT_COLORS['prompt'], style='bold'):
    """Get input with a colored prompt."""
    # Create a bordered input prompt
    content_width = len(prompt) + 2  # Add 2 for padding
    border_line = '─' * content_width
    
    print()
    print_colored(f"┌{border_line}┐", color)
    print_colored(f"│ {prompt} │", color, style=style)
    print_colored(f"└{border_line}┘", color)
    
    # Add a visually distinct input indicator
    return input(colored(" ➤ ", color, style=style))

def print_query_box(title, options=None, color=DEFAULT_COLORS['border']):
    """Print a query box with title and options."""
    # Calculate width based on content
    title_len = len(title)
    
    # Calculate the maximum width needed
    max_width = title_len
    
    if options:
        for option in options:
            option_text = f"{len(options)}. {option}"  # Use the maximum number for width calculation
            max_width = max(max_width, len(option_text))
    
    # Ensure minimum width and add padding
    content_width = max(max_width + 4, 60)
    
    # Create borders with exact width
    border_line = '═' * content_width
    
    # Print query box
    print()
    print_colored(f"╔{border_line}╗", color)
    
    # Print title with proper padding
    title_display = colored(title, DEFAULT_COLORS['section'], style='bold')
    padding = content_width - title_len
    print_colored(f"║ {title_display}{' ' * (padding - 1)}║", color)
    
    if options:
        print_colored(f"╠{border_line}╣", color)
        for i, option in enumerate(options, 1):
            option_text = f"{i}. {option}"
            padding = content_width - len(option_text)
            print_colored(f"║ {colored(option_text, DEFAULT_COLORS['option_text'])}{' ' * (padding - 1)}║", color)
    
    print_colored(f"╚{border_line}╝", color)
