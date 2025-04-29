#!/usr/bin/env python3
"""
Script for displaying camera feed
"""

import sys
from bmt_scripts.webcam.stream import stream_camera

def show_camera(camera_id: int = 0) -> None:
    """
    แสดงภาพจากกล้องเว็บแคม

    Args:
        camera_id (int): ID ของกล้อง (default: 0)
    """
    stream_camera(camera_id)

def main():
    """Main function for showing camera feed"""
    # Get camera ID from command line arguments
    camera_id = 0
    if len(sys.argv) > 1:
        try:
            camera_id = int(sys.argv[1])
        except ValueError:
            print("Camera ID must be a number")
            return
    
    show_camera(camera_id)

if __name__ == "__main__":
    main()