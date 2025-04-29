"""
Example Plugin for BMT Open Python Scripts
"""

import click
from rich.console import Console

console = Console()


def register(plugin_manager):
    """ลงทะเบียน plugin กับระบบ"""

    @plugin_manager.main.command()
    def example():
        """ตัวอย่างคำสั่งจาก plugin"""
        console.print("[green]นี่คือตัวอย่างคำสั่งจาก plugin[/green]")
        console.print("คุณสามารถเพิ่มคำสั่งใหม่ได้โดยการสร้าง plugin ใหม่")
