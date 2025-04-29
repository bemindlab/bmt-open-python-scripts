#!/usr/bin/env python3
"""
BMT Open Python Scripts - CLI
"""

import importlib.util
import logging.config
import os
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

import click
from rich.console import Console

from bmt_scripts.config.settings import (
    LOGGING_CONFIG,
    PLUGIN_DIR,
    PROJECT_ROOT,
    SCRIPTS_DIR,
)
from bmt_scripts.plugins.plugin_manager import PluginManager

# ตั้งค่า logging
logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)

console = Console()
plugin_manager = PluginManager()


class ScriptError(Exception):
    """Custom exception for script-related errors"""

    pass


@click.group()
def main():
    """BMT Open Python Scripts CLI"""
    pass


@main.command()
def version():
    """แสดงเวอร์ชันของแพ็คเกจ"""
    from bmt_scripts import __version__

    console.print(f"BMT Open Python Scripts version: {__version__}")


@main.command()
@click.option(
    "--script",
    "-s",
    help="ชื่อสคริปต์ที่ต้องการรัน (เช่น webcam.show, git.commit-summary)",
)
def run(script: Optional[str]) -> None:
    """รันสคริปต์ที่เลือก"""
    try:
        if not script:
            list_available_scripts()
            return

        category, script_name = parse_script_name(script)
        script_path = find_script_path(category, script_name)

        if not script_path:
            raise ScriptError(f"ไม่พบสคริปต์ '{script}'")

        execute_script(script_path, script)

    except ScriptError as e:
        logger.error(str(e))
        console.print(f"[red]{str(e)}[/red]")
    except Exception as e:
        logger.exception("เกิดข้อผิดพลาดที่ไม่คาดคิด")
        console.print(f"[red]เกิดข้อผิดพลาด: {str(e)}[/red]")


@main.command()
def plugins():
    """แสดงรายการ plugins ที่มีทั้งหมด"""
    plugin_list = plugin_manager.list_plugins()
    if not plugin_list:
        console.print("[yellow]ไม่พบ plugins ที่ติดตั้ง[/yellow]")
        return

    console.print("[bold green]รายการ plugins ที่มีทั้งหมด:[/bold green]")
    for plugin in plugin_list:
        console.print(f"  - {plugin}")


def parse_script_name(script: str) -> tuple[str, str]:
    """แยกชื่อหมวดหมู่และชื่อสคริปต์"""
    parts = script.split(".")
    if len(parts) != 2:
        raise ScriptError(
            "รูปแบบชื่อสคริปต์ไม่ถูกต้อง กรุณาระบุในรูปแบบ 'หมวดหมู่.ชื่อสคริปต์'"
        )
    return parts[0], parts[1]


def execute_script(script_path: str, script_name: str) -> None:
    """รันสคริปต์ที่ระบุ"""
    console.print(f"[green]กำลังรันสคริปต์: {script_name}[/green]")

    # กรอง arguments ที่ไม่จำเป็น
    args = [arg for arg in sys.argv[3:] if arg != script_name]

    # ตั้งค่า environment
    env = setup_environment()

    try:
        subprocess.run([sys.executable, script_path] + args, check=True, env=env)
    except subprocess.CalledProcessError as e:
        raise ScriptError(f"เกิดข้อผิดพลาดในการรันสคริปต์: {str(e)}")


def setup_environment() -> Dict[str, str]:
    """ตั้งค่า environment variables"""
    env = os.environ.copy()
    if "PYTHONPATH" in env:
        env["PYTHONPATH"] = f"{PROJECT_ROOT}:{env['PYTHONPATH']}"
    else:
        env["PYTHONPATH"] = str(PROJECT_ROOT)
    return env


def find_script_path(category: str, script_name: str) -> Optional[str]:
    """ค้นหาเส้นทางของสคริปต์"""
    category_dir = SCRIPTS_DIR / category
    if not category_dir.exists():
        return None

    for file in category_dir.glob("*.py"):
        if file.stem == script_name:
            return str(file)

    return None


def list_available_scripts() -> None:
    """แสดงรายการสคริปต์ที่มีทั้งหมด"""
    if not SCRIPTS_DIR.exists():
        raise ScriptError("ไม่พบโฟลเดอร์ scripts")

    console.print("[bold green]รายการสคริปต์ที่มีทั้งหมด:[/bold green]")

    for category_dir in SCRIPTS_DIR.iterdir():
        if not category_dir.is_dir():
            continue

        category = category_dir.name
        console.print(f"\n[bold blue]{category}:[/bold blue]")

        for script_file in category_dir.glob("*.py"):
            script_name = script_file.stem
            console.print(f"  - {category}.{script_name}")

    console.print("\n[bold]วิธีการใช้งาน:[/bold]")
    console.print("  bmtlab run -s หมวดหมู่.ชื่อสคริปต์ [พารามิเตอร์เพิ่มเติม]")


if __name__ == "__main__":
    main()
