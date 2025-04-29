#!/usr/bin/env python3
"""
สคริปต์สำหรับบันทึกวิดีโอจากกล้อง
"""

import os
import sys
from datetime import datetime
from typing import Optional, Tuple

import cv2

from bmt_scripts.config import WEBCAM_CONFIG


def record_video(
    camera_id: int = 0,
    output_dir: str = "_output_/recordings",
    duration: Optional[int] = None,
    frame_width: int = 1280,
    frame_height: int = 720,
    fps: float = 30.0,
) -> str:
    """
    บันทึกวิดีโอจากกล้องเว็บแคม

    Args:
        camera_id (int): ID ของกล้อง (default: 0)
        output_dir (str): โฟลเดอร์สำหรับเก็บไฟล์วิดีโอ (default: "recordings")
        duration (Optional[int]): ระยะเวลาบันทึกเป็นวินาที (default: None - บันทึกจนกว่าจะกดปุ่มหยุด)
        frame_width (int): ความกว้างของภาพ (default: 1280)
        frame_height (int): ความสูงของภาพ (default: 720)
        fps (float): เฟรมต่อวินาที (default: 30.0)

    Returns:
        str: พาธของไฟล์วิดีโอที่บันทึก
    """
    # สร้างโฟลเดอร์สำหรับเก็บไฟล์วิดีโอ
    os.makedirs(output_dir, exist_ok=True)

    # เปิดกล้อง
    cap = cv2.VideoCapture(camera_id)
    if not cap.isOpened():
        raise RuntimeError(f"ไม่สามารถเปิดกล้อง ID {camera_id} ได้")

    # ตั้งค่ากล้อง
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)
    cap.set(cv2.CAP_PROP_FPS, fps)

    # สร้างชื่อไฟล์วิดีโอ
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = os.path.join(output_dir, f"recording_{timestamp}.mp4")

    # สร้าง VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    writer = cv2.VideoWriter(output_file, fourcc, fps, (frame_width, frame_height))

    print(f"กำลังบันทึกวิดีโอจากกล้อง ID {camera_id}")
    print("กด 'q' เพื่อหยุดบันทึก")

    start_time = datetime.now()

    try:
        while True:
            # อ่านภาพจากกล้อง
            ret, frame = cap.read()
            if not ret:
                raise RuntimeError("ไม่สามารถอ่านภาพจากกล้องได้")

            # บันทึกภาพลงในไฟล์วิดีโอ
            writer.write(frame)

            # แสดงภาพ
            cv2.imshow("Recording", frame)

            # ตรวจสอบระยะเวลาบันทึก
            if duration is not None:
                elapsed_time = (datetime.now() - start_time).total_seconds()
                if elapsed_time >= duration:
                    print(f"บันทึกครบ {duration} วินาทีแล้ว")
                    break

            # ตรวจสอบการกดปุ่มหยุด
            if cv2.waitKey(1) & 0xFF == ord("q"):
                print("หยุดบันทึก")
                break

    finally:
        # ปิดกล้องและหน้าต่าง
        cap.release()
        writer.release()
        cv2.destroyAllWindows()

        # แสดงข้อมูลไฟล์วิดีโอ
        if os.path.exists(output_file):
            file_size = os.path.getsize(output_file) / (1024 * 1024)  # แปลงเป็น MB
            print(f"บันทึกวิดีโอเรียบร้อยแล้ว: {output_file}")
            print(f"ขนาดไฟล์: {file_size:.2f} MB")

        return output_file


def get_recording_info(video_path: str) -> Tuple[int, int, float, float]:
    """
    ดึงข้อมูลของไฟล์วิดีโอ

    Args:
        video_path (str): พาธของไฟล์วิดีโอ

    Returns:
        Tuple[int, int, float, float]: ความกว้าง, ความสูง, FPS และระยะเวลาของวิดีโอ
    """
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise RuntimeError(f"ไม่สามารถเปิดไฟล์วิดีโอ {video_path} ได้")

    try:
        # ดึงข้อมูลความละเอียดและ FPS
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = cap.get(cv2.CAP_PROP_FPS)

        # คำนวณระยะเวลาของวิดีโอ
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        duration = frame_count / fps

        return width, height, fps, duration

    finally:
        cap.release()


def main():
    """
    ฟังก์ชันหลักสำหรับบันทึกวิดีโอจากกล้อง
    """
    # รับพารามิเตอร์จาก command line arguments
    camera_id = 0
    output_dir = "_output_/recordings"
    duration = 60

    if len(sys.argv) > 1:
        try:
            camera_id = int(sys.argv[1])
        except ValueError:
            print("ID ของกล้องต้องเป็นตัวเลข")
            return

    if len(sys.argv) > 2:
        output_dir = sys.argv[2]

    if len(sys.argv) > 3:
        try:
            duration = int(sys.argv[3])
        except ValueError:
            print("ระยะเวลาต้องเป็นตัวเลข")
            return

    record_video(camera_id, output_dir, duration)


if __name__ == "__main__":
    main()
