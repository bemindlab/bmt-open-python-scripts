#!/usr/bin/env python3
"""
ทดสอบการตั้งค่า configuration
"""

import os
import pytest
from scripts.config import get_config, validate_config, WEBCAM_CONFIG, GIT_CONFIG, AUTOGEN_CONFIG

def test_get_config():
    """ทดสอบฟังก์ชัน get_config"""
    config = get_config()
    
    # ตรวจสอบว่ามีการตั้งค่าทั้งหมดครบถ้วน
    assert "env_vars" in config
    assert "webcam" in config
    assert "git" in config
    assert "autogen" in config
    
    # ตรวจสอบการตั้งค่ากล้องเว็บแคม
    assert config["webcam"]["default_camera"] == WEBCAM_CONFIG["default_camera"]
    assert config["webcam"]["frame_width"] == WEBCAM_CONFIG["frame_width"]
    assert config["webcam"]["frame_height"] == WEBCAM_CONFIG["frame_height"]
    assert config["webcam"]["fps"] == WEBCAM_CONFIG["fps"]
    
    # ตรวจสอบการตั้งค่า Git
    assert config["git"]["max_commits"] == GIT_CONFIG["max_commits"]
    assert "*.log" in config["git"]["exclude_patterns"]
    assert "*.tmp" in config["git"]["exclude_patterns"]
    assert "__pycache__" in config["git"]["exclude_patterns"]
    
    # ตรวจสอบการตั้งค่า AutoGen
    assert config["autogen"]["model"] == AUTOGEN_CONFIG["model"]
    assert config["autogen"]["temperature"] == AUTOGEN_CONFIG["temperature"]
    assert config["autogen"]["max_tokens"] == AUTOGEN_CONFIG["max_tokens"]

def test_validate_config(monkeypatch):
    """ทดสอบฟังก์ชัน validate_config"""
    # จำลองการตั้งค่า OPENAI_API_KEY
    monkeypatch.setenv("OPENAI_API_KEY", "test-api-key")
    
    # ตรวจสอบว่าการตั้งค่าถูกต้อง
    assert validate_config() is True
    
    # จำลองการไม่ตั้งค่า OPENAI_API_KEY
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    
    # ตรวจสอบว่าการตั้งค่าไม่ถูกต้อง
    assert validate_config() is False 