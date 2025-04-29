#!/usr/bin/env python3
"""
Module for screen capture functionality

Note: This module requires the following packages:
- Pillow (PIL): pip install Pillow
"""

import os
import sys
from datetime import datetime
try:
    from PIL import ImageGrab
except ImportError:
    print("Error: Pillow package is required. Please install it using:")
    print("pip install Pillow")
    sys.exit(1)

class Screen:
    """Class for handling screen capture operations"""
    
    def __init__(self, output_dir: str = "_output_/screenshots"):
        """
        Initialize Screen class
        
        Args:
            output_dir (str): Directory to save screenshots
        """
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
    
    def save_image(self, region: tuple = None) -> str:
        """
        Capture and save screenshot
        
        Args:
            region (tuple, optional): Region to capture (left, top, width, height)
            
        Returns:
            str: Path to saved image
        """
        # Generate filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"screenshot_{timestamp}.png"
        filepath = os.path.join(self.output_dir, filename)
        
        # Capture screenshot
        screenshot = ImageGrab.grab(bbox=region)
        
        # Save image
        screenshot.save(filepath)
        
        return filepath
    
    def capture_region(self, x: int, y: int, width: int, height: int) -> str:
        """
        Capture specific region of screen
        
        Args:
            x (int): X coordinate of region
            y (int): Y coordinate of region
            width (int): Width of region
            height (int): Height of region
            
        Returns:
            str: Path to saved image
        """
        return self.save_image(region=(x, y, width, height))
    
    def capture_fullscreen(self) -> str:
        """
        Capture full screen
        
        Returns:
            str: Path to saved image
        """
        return self.save_image() 