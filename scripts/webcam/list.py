#!/usr/bin/env python3
"""
สคริปต์สำหรับแสดงรายการเว็บแคมที่มีอยู่ในคอมพิวเตอร์
"""

import cv2
import sys


def list_webcams():
    """
    แสดงรายการเว็บแคมที่มีอยู่ในคอมพิวเตอร์
    """
    print("กำลังค้นหาเว็บแคมที่มีอยู่ในคอมพิวเตอร์...")
    
    # ตรวจสอบเว็บแคมตั้งแต่ index 0 ถึง 10
    available_webcams = []
    for i in range(10):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            # อ่านข้อมูลจากเว็บแคม
            ret, frame = cap.read()
            if ret:
                # รับข้อมูลขนาดของเฟรม
                height, width = frame.shape[:2]
                # รับข้อมูล FPS
                fps = cap.get(cv2.CAP_PROP_FPS)
                # รับข้อมูลชื่ออุปกรณ์ (ถ้ามี)
                device_name = f"Webcam {i}"
                try:
                    device_name = cap.getBackendName()
                except:
                    pass
                
                available_webcams.append({
                    "index": i,
                    "name": device_name,
                    "resolution": f"{width}x{height}",
                    "fps": fps
                })
            
            # ปิดการเชื่อมต่อกับเว็บแคม
            cap.release()
    
    # แสดงรายการเว็บแคมที่พบ
    if available_webcams:
        print(f"พบเว็บแคมทั้งหมด {len(available_webcams)} อุปกรณ์:")
        for webcam in available_webcams:
            print(f"  - Index: {webcam['index']}, ชื่อ: {webcam['name']}, ความละเอียด: {webcam['resolution']}, FPS: {webcam['fps']}")
    else:
        print("ไม่พบเว็บแคมในคอมพิวเตอร์")


if __name__ == "__main__":
    try:
        list_webcams()
    except KeyboardInterrupt:
        print("\nยกเลิกการทำงาน")
        sys.exit(0)
    except Exception as e:
        print(f"เกิดข้อผิดพลาด: {e}")
        sys.exit(1)
