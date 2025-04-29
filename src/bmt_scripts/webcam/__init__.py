"""
Webcam Module

โมดูลสำหรับจัดการการทำงานกับกล้องเว็บแคม
"""

from .record import record_video
from .stream import stream_camera

__all__ = ["stream_camera", "record_video"]
