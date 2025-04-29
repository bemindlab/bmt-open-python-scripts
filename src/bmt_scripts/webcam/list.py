#!/usr/bin/env python3
"""
สคริปต์สำหรับแสดงรายการกล้องที่มีในระบบ
"""

from typing import List, Dict, Any
import cv2

def list_cameras() -> List[Dict[str, Any]]:
    """
    แสดงรายการกล้องที่มีในระบบ
    
    Returns:
        List[Dict[str, Any]]: รายการกล้องที่มีในระบบ
    """
    available_cameras = []
    
    # Try to open cameras from index 0 to 10
    for i in range(10):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            # Get camera properties
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            fps = cap.get(cv2.CAP_PROP_FPS)
            
            camera_info = {
                "id": i,
                "width": width,
                "height": height,
                "fps": fps
            }
            
            available_cameras.append(camera_info)
            cap.release()
    
    return available_cameras

def main():
    """
    ฟังก์ชันหลักสำหรับแสดงรายการกล้อง
    """
    print("กำลังค้นหาเว็บแคมที่มีอยู่ในคอมพิวเตอร์...")
    cameras = list_cameras()
    
    if not cameras:
        print("ไม่พบเว็บแคมในคอมพิวเตอร์")
        return
    
    print(f"พบเว็บแคมทั้งหมด {len(cameras)} อุปกรณ์:")
    for camera in cameras:
        print(f"- กล้อง ID: {camera['id']}")
        print(f"  ความละเอียด: {camera['width']}x{camera['height']}")
        print(f"  FPS: {camera['fps']}")

if __name__ == "__main__":
    main()
