"""
Window utility functions for responsive GUI layout
"""


def setup_responsive_window(master):
    """Configure window size based on screen resolution
    
    Args:
        master: The Tkinter root/master window
        
    Returns:
        dict: Window scale configuration with width, height, padding, and font_scale
    """
    # Get screen dimensions
    screen_width = master.winfo_screenwidth()
    screen_height = master.winfo_screenheight()
    
    # Calculate responsive dimensions based on screen size
    # Target: 60-70% of screen width, 80-85% of screen height (with max limits)
    if screen_width <= 1366:  # Small laptops (13-14 inch)
        base_width = 800
        base_height = 900
        min_width = 750
        min_height = 850
    elif screen_width <= 1920:  # Standard laptops/displays (15-16 inch, 1080p)
        base_width = 900
        base_height = 1000
        min_width = 850
        min_height = 950
    elif screen_width <= 2560:  # Large displays (1440p, 27-inch)
        base_width = 1000
        base_height = 1100
        min_width = 950
        min_height = 1050
    else:  # Ultra-wide/4K displays (2560p+, 32-inch+)
        base_width = 1200
        base_height = 1200
        min_width = 1100
        min_height = 1100
    
    # Ensure window fits on screen (max 85% height, 70% width)
    max_width = int(screen_width * 0.70)
    max_height = int(screen_height * 0.85)
    
    window_width = min(base_width, max_width)
    window_height = min(base_height, max_height)
    
    # Adjust min sizes to not exceed actual window size
    min_width = min(min_width, window_width - 50)
    min_height = min(min_height, window_height - 50)
    
    # Center window on screen
    x = max(0, (screen_width - window_width) // 2)
    y = max(0, (screen_height - window_height) // 2)
    
    # Set geometry and constraints
    master.geometry(f"{window_width}x{window_height}+{x}+{y}")
    master.resizable(True, True)
    master.minsize(min_width, min_height)
    
    # Return scale configuration for responsive components
    return {
        "width": window_width,
        "height": window_height,
        "padding": 20 if window_height < 900 else 30,
        "font_scale": 0.9 if window_height < 900 else 1.0,
        "image_scale": 0.6 if window_height < 900 else 1.0,
        "component_spacing": 10 if window_height < 900 else 30,
        "card_spacing": 12 if window_height < 900 else 20,
        "card_padding": 15 if window_height < 900 else 20
    }


def apply_macos_fix(master):
    """Workaround for macOS Sonoma button click bug
    
    Args:
        master: The Tkinter root/master window
    """
    import platform
    if platform.system() == "Darwin":  # macOS only
        try:
            x = master.winfo_x()
            y = master.winfo_y()
            master.geometry(f"+{x+1}+{y}")
            master.update()
            # Move it back to original position
            master.geometry(f"+{x}+{y}")
        except:
            pass  # Silently fail if there's any issue
