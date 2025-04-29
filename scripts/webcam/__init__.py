"""
Webcam Module

โมดูลสำหรับจัดการการทำงานกับกล้องเว็บแคม
"""

from .stream import stream_camera
from .record import record_video

__all__ = ['stream_camera', 'record_video'] 