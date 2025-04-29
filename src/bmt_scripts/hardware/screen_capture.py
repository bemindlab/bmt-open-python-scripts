#!/usr/bin/env python3
"""
Script for capturing screenshots
"""

import sys

from bmt_libs.hardware import Screen


def main():
    """Main function for capturing screen"""
    screen = Screen()
    image_path = screen.save_image()
    print(f"Screenshot captured and saved to: {image_path}")


if __name__ == "__main__":
    main()
