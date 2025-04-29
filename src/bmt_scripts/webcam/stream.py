#!/usr/bin/env python3
"""
Stream Module

โมดูลสำหรับการสตรีมภาพจากกล้องเว็บแคม
"""

import cv2
import sys
import os
from datetime import datetime
from bmt_scripts.config import WEBCAM_CONFIG
from typing import Optional, Tuple

def stream_camera(
    camera_id: int = 0,
    window_name: str = "Camera Stream",
    exit_key: str = 'q'
) -> None:
    """
    สตรีมภาพจากกล้องเว็บแคม

    Args:
        camera_id (int): ID ของกล้อง (default: 0)
        window_name (str): ชื่อหน้าต่างแสดงภาพ (default: "Camera Stream")
        exit_key (str): ปุ่มสำหรับออกจากสตรีม (default: 'q')
    """
    # เปิดกล้อง
    cap = cv2.VideoCapture(camera_id)
    if not cap.isOpened():
        raise RuntimeError(f"ไม่สามารถเปิดกล้อง ID {camera_id} ได้")

    try:
        while True:
            # อ่านภาพจากกล้อง
            ret, frame = cap.read()
            if not ret:
                raise RuntimeError("ไม่สามารถอ่านภาพจากกล้องได้")

            # แสดงภาพ
            cv2.imshow(window_name, frame)

            # ตรวจสอบการกดปุ่มออก
            if cv2.waitKey(1) & 0xFF == ord(exit_key):
                break

    finally:
        # ปิดกล้องและหน้าต่าง
        cap.release()
        cv2.destroyAllWindows()

def get_camera_info(camera_id: int = 0) -> Tuple[int, int, float]:
    """
    ดึงข้อมูลของกล้อง

    Args:
        camera_id (int): ID ของกล้อง (default: 0)

    Returns:
        Tuple[int, int, float]: ความกว้าง, ความสูง และ FPS ของกล้อง
    """
    cap = cv2.VideoCapture(camera_id)
    if not cap.isOpened():
        raise RuntimeError(f"ไม่สามารถเปิดกล้อง ID {camera_id} ได้")

    try:
        # ดึงข้อมูลความละเอียดและ FPS
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = cap.get(cv2.CAP_PROP_FPS)

        return width, height, fps

    finally:
        cap.release()

def list_available_cameras(max_cameras: int = 10) -> list:
    """
    แสดงรายการกล้องที่ใช้งานได้

    Args:
        max_cameras (int): จำนวนกล้องสูงสุดที่จะตรวจสอบ (default: 10)

    Returns:
        list: รายการ ID ของกล้องที่ใช้งานได้
    """
    available_cameras = []
    
    for i in range(max_cameras):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            available_cameras.append(i)
            cap.release()
    
    return available_cameras

def main():
    """
    ฟังก์ชันหลักสำหรับสตรีมภาพจากกล้อง
    """
    # รับพารามิเตอร์จาก command line arguments
    camera_id = 0
    output_dir = "streams"
    
    if len(sys.argv) > 1:
        try:
            camera_id = int(sys.argv[1])
        except ValueError:
            print("ID ของกล้องต้องเป็นตัวเลข")
            return
    
    if len(sys.argv) > 2:
        output_dir = sys.argv[2]
    
    stream_camera(camera_id, output_dir)

if __name__ == "__main__":
    main() 