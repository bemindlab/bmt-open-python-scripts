#!/usr/bin/env python3
"""
โมดูลสำหรับจัดการการทำงานกับเว็บแคม
"""

import datetime
import os
import platform
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union

import cv2
import numpy as np


class Webcam:
    """
    คลาสสำหรับจัดการเว็บแคม
    """

    def __init__(self, camera_index: int):
        """
        สร้างอ็อบเจ็กต์ Webcam

        Args:
            camera_index (int): ดัชนีของกล้อง
        """
        self.camera_index = camera_index
        self.cap = None
        self.writer = None
        self.is_recording = False
        
        # กำหนดไดเรกทอรีตามระบบปฏิบัติการ
        if platform.system() == "Darwin":  # macOS
            self.save_dir = str(Path.home() / "Pictures" / "webcam")
        elif platform.system() == "Windows":
            self.save_dir = str(Path.home() / "Pictures" / "webcam")
        else:  # Linux และอื่นๆ
            self.save_dir = str(Path.home() / "Pictures" / "webcam")
            
        # สร้างไดเรกทอรีถ้ายังไม่มี
        try:
            Path(self.save_dir).mkdir(parents=True, exist_ok=True)
        except Exception as e:
            # ถ้าไม่สามารถสร้างไดเรกทอรีได้ ให้ใช้ไดเรกทอรีชั่วคราว
            self.save_dir = str(Path(os.getcwd()) / "tmp" / "webcam")
            Path(self.save_dir).mkdir(parents=True, exist_ok=True)

    def open(self) -> bool:
        """
        เปิดการเชื่อมต่อกับเว็บแคม

        Returns:
            bool: True ถ้าเปิดสำเร็จ, False ถ้าไม่สำเร็จ
        """
        try:
            self.cap = cv2.VideoCapture(self.camera_index)
            if not self.cap.isOpened():
                self.cap = None
                return False
            return True
        except Exception:
            self.cap = None
            return False

    def close(self) -> None:
        """
        ปิดการเชื่อมต่อกับเว็บแคม
        """
        if self.cap is not None:
            self.cap.release()
            self.cap = None

    def read_frame(self) -> Tuple[bool, Optional[np.ndarray]]:
        """
        อ่านเฟรมจากเว็บแคม

        Returns:
            Tuple[bool, Optional[np.ndarray]]: (สถานะการอ่าน, เฟรมที่อ่านได้)
        """
        if self.cap is None or not self.cap.isOpened():
            raise RuntimeError("กล้องยังไม่ได้เปิด")
        return self.cap.read()

    def get_property(self, prop_id: int) -> float:
        """
        รับค่าคุณสมบัติของเว็บแคม

        Args:
            prop_id (int): รหัสคุณสมบัติ

        Returns:
            float: ค่าคุณสมบัติ
        """
        if self.cap is None or not self.cap.isOpened():
            raise RuntimeError("กล้องยังไม่ได้เปิด")
        return self.cap.get(prop_id)

    def save_image(self, frame: np.ndarray, filename: Optional[str] = None) -> str:
        """
        บันทึกเฟรมเป็นภาพ

        Args:
            frame (np.ndarray): เฟรมที่ต้องการบันทึก
            filename (Optional[str]): ชื่อไฟล์ (ถ้าไม่ระบุจะใช้เวลาปัจจุบัน)

        Returns:
            str: พาธของไฟล์ที่บันทึก
        """
        if filename is None:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{timestamp}.jpg"

        save_path = os.path.join(self.save_dir, filename)
        cv2.imwrite(save_path, frame)
        return save_path

    def start_recording(self, filename: Optional[str] = None) -> str:
        """
        เริ่มบันทึกวิดีโอ

        Args:
            filename (Optional[str]): ชื่อไฟล์ (ถ้าไม่ระบุจะใช้เวลาปัจจุบัน)

        Returns:
            str: พาธของไฟล์ที่บันทึก
        """
        if self.is_recording:
            raise RuntimeError("กำลังบันทึกวิดีโออยู่")

        if self.cap is None or not self.cap.isOpened():
            raise RuntimeError("ไม่สามารถเริ่มบันทึกวิดีโอได้ เนื่องจากไม่ได้เปิดการเชื่อมต่อกับเว็บแคม")

        if filename is None:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{timestamp}.mp4"

        save_path = os.path.join(self.save_dir, filename)

        # รับข้อมูลข้อมูลขนาดของเฟรม
        width = int(self.get_property(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(self.get_property(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = int(self.get_property(cv2.CAP_PROP_FPS))

        # สร้าง VideoWriter
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.writer = cv2.VideoWriter(save_path, fourcc, fps, (width, height))
        self.is_recording = True

        return save_path

    def stop_recording(self) -> None:
        """
        หยุดบันทึกวิดีโอ
        """
        if not self.is_recording:
            raise RuntimeError("ไม่ได้กำลังบันทึกวิดีโอ")

        if self.writer is not None:
            self.writer.release()
            self.writer = None
            self.is_recording = False

    def write_frame(self, frame: np.ndarray) -> None:
        """
        เขียนเฟรมลงในไฟล์วิดีโอ

        Args:
            frame (np.ndarray): เฟรมที่ต้องการบันทึก
        """
        if not self.is_recording:
            raise RuntimeError("ไม่ได้กำลังบันทึกวิดีโอ")

        if self.writer is not None:
            self.writer.write(frame)

    def __enter__(self):
        """
        เปิดกล้องเมื่อเริ่มใช้งาน context manager
        """
        if not self.open():
            raise RuntimeError("ไม่สามารถเปิดกล้องได้")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        ปิดกล้องเมื่อสิ้นสุดการใช้งาน context manager
        """
        if self.is_recording:
            self.stop_recording()
        self.close()

    @classmethod
    def list_cameras(cls) -> List[Dict[str, Union[int, str, float]]]:
        """
        ค้นหาเว็บแคมที่สามารถใช้งานได้

        Returns:
            List[Dict[str, Union[int, str, float]]]: รายการข้อมูลของเว็บแคมที่ใช้งานได้
        """
        return list_available_webcams()


def list_available_webcams() -> List[Dict[str, Union[int, str, float]]]:
    """
    ค้นหาเว็บแคมที่สามารถใช้งานได้

    Returns:
        List[Dict[str, Union[int, str, float]]]: รายการข้อมูลของเว็บแคมที่ใช้งานได้
    """
    available_webcams = []
    for i in range(3):  # ตรวจสอบกล้อง 3 ตัวแรก
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            # อ่านข้อมูลของเว็บแคม
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            fps = cap.get(cv2.CAP_PROP_FPS)

            # สร้าง dictionary เก็บข้อมูล
            webcam_info = {
                "index": i,
                "name": f"Webcam {i}",  # ชื่อเริ่มต้น
                "resolution": f"{width}x{height}",
                "fps": fps
            }
            available_webcams.append(webcam_info)
        cap.release()
    return available_webcams
