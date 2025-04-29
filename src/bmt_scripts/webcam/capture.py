#!/usr/bin/env python3
"""
สคริปต์สำหรับถ่ายภาพจากกล้อง
"""

import os
import sys
from datetime import datetime
from typing import Optional, Tuple

import cv2

from bmt_scripts.config import WEBCAM_CONFIG


def capture_image(
    camera_id: int = 0,
    output_dir: str = "_output_/captures",
    frame_width: int = 1280,
    frame_height: int = 720,
    show_preview: bool = True,
) -> str:
    """
    ถ่ายภาพจากกล้องเว็บแคม

    Args:
        camera_id (int): ID ของกล้อง (default: 0)
        output_dir (str): โฟลเดอร์สำหรับเก็บไฟล์ภาพ (default: "captures")
        frame_width (int): ความกว้างของภาพ (default: 1280)
        frame_height (int): ความสูงของภาพ (default: 720)
        show_preview (bool): แสดงตัวอย่างภาพก่อนบันทึก (default: True)

    Returns:
        str: พาธของไฟล์ภาพที่บันทึก
    """
    # สร้างโฟลเดอร์สำหรับเก็บไฟล์ภาพ
    os.makedirs(output_dir, exist_ok=True)

    # เปิดกล้อง
    cap = cv2.VideoCapture(camera_id)
    if not cap.isOpened():
        raise RuntimeError(f"ไม่สามารถเปิดกล้อง ID {camera_id} ได้")

    # ตั้งค่ากล้อง
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)

    print(f"กำลังถ่ายภาพจากกล้อง ID {camera_id}")
    print("กด 'Space' เพื่อถ่ายภาพ")
    print("กด 'q' เพื่อออก")

    try:
        while True:
            # อ่านภาพจากกล้อง
            ret, frame = cap.read()
            if not ret:
                raise RuntimeError("ไม่สามารถอ่านภาพจากกล้องได้")

            # แสดงภาพ
            if show_preview:
                cv2.imshow("Camera Preview", frame)

            # รอการกดปุ่ม
            key = cv2.waitKey(1) & 0xFF

            # ถ่ายภาพเมื่อกดปุ่ม Space
            if key == ord(" "):
                # สร้างชื่อไฟล์ภาพ
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_file = os.path.join(output_dir, f"capture_{timestamp}.jpg")

                # บันทึกภาพ
                cv2.imwrite(output_file, frame)

                # แสดงข้อมูลไฟล์ภาพ
                file_size = os.path.getsize(output_file) / 1024  # แปลงเป็น KB
                print(f"บันทึกภาพเรียบร้อยแล้ว: {output_file}")
                print(f"ขนาดไฟล์: {file_size:.2f} KB")
                print(f"ความละเอียด: {frame.shape[1]}x{frame.shape[0]}")

                return output_file

            # ออกจากโปรแกรมเมื่อกดปุ่ม q
            elif key == ord("q"):
                print("ออกจากโปรแกรม")
                break

    finally:
        # ปิดกล้องและหน้าต่าง
        cap.release()
        cv2.destroyAllWindows()

    # ถ้าไม่ได้ถ่ายภาพ ให้คืนค่า None
    return ""


def get_image_info(image_path: str) -> Tuple[int, int, int]:
    """
    ดึงข้อมูลของไฟล์ภาพ

    Args:
        image_path (str): พาธของไฟล์ภาพ

    Returns:
        Tuple[int, int, int]: ความกว้าง, ความสูง และจำนวนช่องสีของภาพ
    """
    image = cv2.imread(image_path)
    if image is None:
        raise RuntimeError(f"ไม่สามารถเปิดไฟล์ภาพ {image_path} ได้")

    height, width, channels = image.shape
    return width, height, channels


def capture_burst(
    camera_id: int = 0,
    output_dir: str = "captures",
    num_images: int = 5,
    interval: float = 1.0,
    frame_width: int = 1280,
    frame_height: int = 720,
) -> list:
    """
    ถ่ายภาพต่อเนื่องหลายภาพ

    Args:
        camera_id (int): ID ของกล้อง (default: 0)
        output_dir (str): โฟลเดอร์สำหรับเก็บไฟล์ภาพ (default: "captures")
        num_images (int): จำนวนภาพที่ต้องการถ่าย (default: 5)
        interval (float): ระยะห่างระหว่างการถ่ายภาพในหน่วยวินาที (default: 1.0)
        frame_width (int): ความกว้างของภาพ (default: 1280)
        frame_height (int): ความสูงของภาพ (default: 720)

    Returns:
        list: รายการพาธของไฟล์ภาพที่บันทึก
    """
    # สร้างโฟลเดอร์สำหรับเก็บไฟล์ภาพ
    os.makedirs(output_dir, exist_ok=True)

    # เปิดกล้อง
    cap = cv2.VideoCapture(camera_id)
    if not cap.isOpened():
        raise RuntimeError(f"ไม่สามารถเปิดกล้อง ID {camera_id} ได้")

    # ตั้งค่ากล้อง
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)

    print(f"กำลังถ่ายภาพต่อเนื่อง {num_images} ภาพ")
    print(f"ระยะห่างระหว่างภาพ: {interval} วินาที")

    captured_files = []

    try:
        for i in range(num_images):
            # อ่านภาพจากกล้อง
            ret, frame = cap.read()
            if not ret:
                raise RuntimeError("ไม่สามารถอ่านภาพจากกล้องได้")

            # สร้างชื่อไฟล์ภาพ
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = os.path.join(output_dir, f"burst_{timestamp}_{i+1}.jpg")

            # บันทึกภาพ
            cv2.imwrite(output_file, frame)
            captured_files.append(output_file)

            # แสดงความคืบหน้า
            print(f"ถ่ายภาพที่ {i+1}/{num_images}: {output_file}")

            # รอตามระยะเวลาที่กำหนด
            cv2.waitKey(int(interval * 1000))

    finally:
        # ปิดกล้อง
        cap.release()

    return captured_files


def main():
    """
    ฟังก์ชันหลักสำหรับถ่ายภาพจากกล้อง
    """
    # รับพารามิเตอร์จาก command line arguments
    camera_id = 0
    output_dir = "_output_/captures"

    if len(sys.argv) > 1:
        try:
            camera_id = int(sys.argv[1])
        except ValueError:
            print("ID ของกล้องต้องเป็นตัวเลข")
            return

    if len(sys.argv) > 2:
        output_dir = sys.argv[2]

    capture_image(camera_id, output_dir)


if __name__ == "__main__":
    main()
