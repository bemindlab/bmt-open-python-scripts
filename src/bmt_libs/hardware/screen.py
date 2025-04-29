#!/usr/bin/env python3
"""
โมดูลสำหรับจัดการการจับภาพหน้าจอและการบันทึกวิดีโอ
"""

import datetime
import os
import platform
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union

import cv2
import numpy as np
import pyautogui


class Screen:
    """
    คลาสสำหรับจัดการการจับภาพหน้าจอและการบันทึกวิดีโอ
    """

    def __init__(self):
        """
        สร้างอ็อบเจ็กต์ Screen
        """
        self.writer = None
        self.is_recording = False

        # กำหนดไดเรกทอรีตามระบบปฏิบัติการ
        if platform.system() == "Darwin":  # macOS
            self.save_dir = str(Path.home() / "Pictures" / "screen")
        elif platform.system() == "Windows":
            self.save_dir = str(Path.home() / "Pictures" / "screen")
        else:  # Linux และอื่นๆ
            self.save_dir = str(Path.home() / "Pictures" / "screen")

        # สร้างไดเรกทอรีถ้ายังไม่มี
        try:
            Path(self.save_dir).mkdir(parents=True, exist_ok=True)
        except Exception:
            # ถ้าไม่สามารถสร้างไดเรกทอรีได้ ให้ใช้ไดเรกทอรีชั่วคราว
            self.save_dir = str(Path(os.getcwd()) / "tmp" / "screen")
            Path(self.save_dir).mkdir(parents=True, exist_ok=True)

        self.screen_size = pyautogui.size()

    def capture_screen(self) -> np.ndarray:
        """
        จับภาพหน้าจอ

        Returns:
            np.ndarray: เฟรมที่จับได้
        """
        # จับภาพหน้าจอด้วย pyautogui
        screenshot = pyautogui.screenshot()
        # แปลงเป็น numpy array
        frame = np.array(screenshot)
        # แปลงจาก RGB เป็น BGR (สำหรับ OpenCV)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        return frame

    def save_image(
        self, frame: Optional[np.ndarray] = None, filename: Optional[str] = None
    ) -> str:
        """
        บันทึกภาพหน้าจอ

        Args:
            frame (Optional[np.ndarray]): เฟรมที่ต้องการบันทึก (ถ้าไม่ระบุจะจับภาพหน้าจอใหม่)
            filename (Optional[str]): ชื่อไฟล์ (ถ้าไม่ระบุจะใช้เวลาปัจจุบัน)

        Returns:
            str: พาธของไฟล์ที่บันทึก
        """
        if frame is None:
            frame = self.capture_screen()

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

        if filename is None:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{timestamp}.mp4"

        save_path = os.path.join(self.save_dir, filename)

        # รับข้อมูลขนาดของหน้าจอ
        width, height = self.screen_size

        # สร้าง VideoWriter
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        fps = 20.0  # กำหนด FPS เริ่มต้น
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

    def write_frame(self, frame: Optional[np.ndarray] = None) -> None:
        """
        เขียนเฟรมลงในไฟล์วิดีโอ

        Args:
            frame (Optional[np.ndarray]): เฟรมที่ต้องการบันทึก (ถ้าไม่ระบุจะจับภาพหน้าจอใหม่)
        """
        if not self.is_recording:
            raise RuntimeError("ไม่ได้กำลังบันทึกวิดีโอ")

        if frame is None:
            frame = self.capture_screen()

        if self.writer is not None:
            self.writer.write(frame)

    def get_screen_info(self) -> Dict[str, Union[str, int]]:
        """
        รับข้อมูลของหน้าจอ

        Returns:
            Dict[str, Union[str, int]]: ข้อมูลของหน้าจอ
        """
        width, height = self.screen_size
        screen_info = {
            "resolution": f"{width}x{height}",
            "width": width,
            "height": height,
        }
        return screen_info


def list_available_screens() -> List[Dict[str, Union[str, int]]]:
    """
    ค้นหาหน้าจอที่สามารถใช้งานได้

    Returns:
        List[Dict[str, Union[str, int]]]: รายการข้อมูลของหน้าจอที่ใช้งานได้
    """
    screen = Screen()
    screen_info = screen.get_screen_info()
    return [screen_info]
