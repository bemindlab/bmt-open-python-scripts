#!/usr/bin/env python3
"""
สคริปต์สำหรับแสดงรายการกล้องที่มีในระบบ
"""

from typing import List, Dict, Any
from lib.hardware.camera import list_available_webcams

def list_cameras() -> List[Dict[str, Any]]:
    """
    แสดงรายการกล้องที่มีในระบบ
    
    Returns:
        List[Dict[str, Any]]: รายการกล้องที่มีในระบบ
    """
    return list_available_webcams()

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
        print(f"- {camera['name']} (ID: {camera['index']})")
        print(f"  ความละเอียด: {camera['resolution']}")
        print(f"  FPS: {camera['fps']}")

if __name__ == "__main__":
    main()
