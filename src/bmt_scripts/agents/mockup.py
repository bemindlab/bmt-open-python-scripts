#!/usr/bin/env python3
"""Mockup agent module."""

import os
import sys
from typing import Any, Dict, List

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from scripts.git.commit_summary import CommitInfo, get_current_commit  # noqa: E402


class MockupAgent:
    """Agent สำหรับสร้าง mockup ข้อมูล."""

    def __init__(self) -> None:
        """Initialize mockup agent."""
        self.commit_info: CommitInfo | None = None

    def get_commit_info(self) -> CommitInfo:
        """ดึงข้อมูล commit ล่าสุด."""
        if not self.commit_info:
            self.commit_info = get_current_commit()
        return self.commit_info

    def generate_mockup(self) -> Dict[str, Any]:
        """สร้าง mockup ข้อมูล."""
        commit = self.get_commit_info()
        return {
            "commit": {
                "hash": commit.hash,
                "author": commit.author,
                "date": commit.date,
                "message": commit.message,
            },
            "files": [],
            "summary": "",
        }
