#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
สคริปต์สำหรับแสดงวิดีโอสตรีมจากเว็บแคม
"""

import argparse
import cv2
import sys
import datetime
import os
from pathlib import Path


def show_webcam(camera_index=0):
    """
    แสดงวิดีโอสตรีมจากเว็บแคม
    
    Args:
        camera_index (int): ดัชนีของกล้องเว็บแคม (ค่าเริ่มต้นคือ 0)
    """
    # เปิดการเชื่อมต่อกับกล้องเว็บแคม
    cap = cv2.VideoCapture(camera_index)
    
    # ตรวจสอบว่าสามารถเปิดกล้องได้หรือไม่
    if not cap.isOpened():
        print(f"ไม่สามารถเปิดกล้องเว็บแคมที่ดัชนี {camera_index} ได้")
        return
    
    print(f"กำลังแสดงวิดีโอสตรีมจากกล้องเว็บแคมที่ดัชนี {camera_index}")
    print("กด 'q' เพื่อออกจากโปรแกรม")
    print("กด 'c' เพื่อบันทึกภาพ")
    
    # สร้างโฟลเดอร์สำหรับเก็บภาพถ่าย
    save_dir = os.path.expanduser("~/Pictures/webcam")
    Path(save_dir).mkdir(parents=True, exist_ok=True)
    
    try:
        while True:
            # อ่านเฟรมจากกล้อง
            ret, frame = cap.read()
            
            # ตรวจสอบว่าอ่านเฟรมได้หรือไม่
            if not ret:
                print("ไม่สามารถอ่านเฟรมจากกล้องได้")
                break
            
            # แสดงเฟรม
            cv2.imshow('Webcam', frame)
            
            # รอการกดปุ่ม (1 มิลลิวินาที)
            key = cv2.waitKey(1) & 0xFF
            
            # ถ้ากด 'q' ให้ออกจากลูป
            if key == ord('q'):
                break
            
            # ถ้ากด 'c' ให้บันทึกเฟรมเป็นภาพ ไปที่โฟลเดอร์ ~/Pictures/webcam/{timestamp}.jpg
            if key == ord('c'):
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                save_path = os.path.join(save_dir, f"{timestamp}.jpg")
                cv2.imwrite(save_path, frame)
                print(f"ภาพถ่ายถูกบันทึกเป็น '{save_path}'")
    
    finally:
        # คืนทรัพยากร
        cap.release()
        cv2.destroyAllWindows()


def main():
    """ฟังก์ชันหลัก"""
    parser = argparse.ArgumentParser(description='แสดงวิดีโอสตรีมจากเว็บแคม')
    parser.add_argument('--index', type=int, default=0, help='ดัชนีของกล้องเว็บแคม (ค่าเริ่มต้นคือ 0)')
    
    args = parser.parse_args()
    
    try:
        show_webcam(args.index)
    except KeyboardInterrupt:
        print("\nโปรแกรมถูกยกเลิกโดยผู้ใช้")
        sys.exit(0)
    except Exception as e:
        print(f"เกิดข้อผิดพลาด: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
