#!/usr/bin/env python3
"""
การตั้งค่า configuration สำหรับ BMT Open Python Scripts
"""

import os
from dotenv import load_dotenv

# โหลด environment variables จากไฟล์ .env
load_dotenv()

# Configuration สำหรับสคริปต์ต่างๆ
WEBCAM_CONFIG = {
    "default_camera": 0,
    "frame_width": 640,
    "frame_height": 480,
    "fps": 30,
}

GIT_CONFIG = {
    "max_commits": 10,
    "exclude_patterns": [
        "*.log",
        "*.tmp",
        "__pycache__",
    ],
}

AUTOGEN_CONFIG = {
    "model": "gpt-4",
    "temperature": 0.7,
    "max_tokens": 2000,
}

def get_config():
    """
    ดึงการตั้งค่าทั้งหมด
    
    Returns:
        dict: การตั้งค่าทั้งหมด
    """
    return {
        "env_vars": {
            "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY"),
        },
        "webcam": WEBCAM_CONFIG,
        "git": GIT_CONFIG,
        "autogen": AUTOGEN_CONFIG,
    }

def validate_config():
    """
    ตรวจสอบการตั้งค่า
    
    Returns:
        bool: True ถ้าการตั้งค่าถูกต้อง, False ถ้าไม่ถูกต้อง
    """
    # ตรวจสอบ environment variables
    if not os.getenv("OPENAI_API_KEY"):
        return False
    
    return True

if __name__ == "__main__":
    # ตัวอย่างการใช้งาน
    config = get_config()
    print("Current configuration:")
    for section, settings in config.items():
        print(f"\n{section.upper()}:")
        for key, value in settings.items():
            print(f"  {key}: {value}")
    
    # ตรวจสอบการตั้งค่า
    if validate_config():
        print("\nConfiguration is valid")
    else:
        print("\nConfiguration validation failed") 