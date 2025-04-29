#!/usr/bin/env python3

"""
สคริปต์สำหรับแสดงภาพจากกล้อง
"""

import cv2
import sys
from scripts.config import WEBCAM_CONFIG

def show_camera(camera_id: int = 0):
    """
    แสดงภาพจากกล้องที่ระบุ
    
    Args:
        camera_id (int): ID ของกล้องที่ต้องการแสดงภาพ
    """
    # เปิดกล้อง
    cap = cv2.VideoCapture(camera_id)
    if not cap.isOpened():
        print(f"ไม่สามารถเปิดกล้อง ID {camera_id} ได้")
        return
    
    # ตั้งค่ากล้องตาม configuration
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, WEBCAM_CONFIG["frame_width"])
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, WEBCAM_CONFIG["frame_height"])
    cap.set(cv2.CAP_PROP_FPS, WEBCAM_CONFIG["fps"])
    
    print(f"กำลังแสดงภาพจากกล้อง ID {camera_id}")
    print("กด 'q' เพื่อออก")
    
    try:
        while True:
            # อ่านภาพจากกล้อง
            ret, frame = cap.read()
            if not ret:
                print("ไม่สามารถอ่านภาพจากกล้องได้")
                break
            
            # แสดงภาพ
            cv2.imshow("Camera", frame)
            
            # รอการกดปุ่ม
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
    
    finally:
        # ปิดกล้องและหน้าต่าง
        cap.release()
        cv2.destroyAllWindows()

def main():
    """
    ฟังก์ชันหลักสำหรับแสดงภาพจากกล้อง
    """
    # รับ ID ของกล้องจาก command line argument
    camera_id = 0
    if len(sys.argv) > 1:
        try:
            camera_id = int(sys.argv[1])
        except ValueError:
            print("ID ของกล้องต้องเป็นตัวเลข")
            return
    
    show_camera(camera_id)

if __name__ == "__main__":
    main()
