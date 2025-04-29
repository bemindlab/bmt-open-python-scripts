#!/usr/bin/env python3
"""
BMT Open Python Scripts - CLI
"""

import click
from rich.console import Console
import os
import sys
import importlib.util
import subprocess
from pathlib import Path

console = Console()

@click.group()
def main():
    """BMT Open Python Scripts CLI"""
    pass

@main.command()
def version():
    """แสดงเวอร์ชันของแพ็คเกจ"""
    from bmt_open_python_scripts import __version__
    console.print(f"BMT Open Python Scripts version: {__version__}")

@main.command()
@click.option('--script', '-s', help='ชื่อสคริปต์ที่ต้องการรัน (เช่น webcam.show, git.commit-summary)')
def run(script):
    """รันสคริปต์ที่เลือก"""
    if not script:
        # แสดงรายการสคริปต์ที่มีทั้งหมด
        list_available_scripts()
        return
    
    # แยกชื่อหมวดหมู่และชื่อสคริปต์
    parts = script.split('.')
    if len(parts) != 2:
        console.print(f"[red]รูปแบบชื่อสคริปต์ไม่ถูกต้อง กรุณาระบุในรูปแบบ 'หมวดหมู่.ชื่อสคริปต์'[/red]")
        return
    
    category, script_name = parts
    
    # ตรวจสอบว่าสคริปต์มีอยู่จริงหรือไม่
    script_path = find_script_path(category, script_name)
    if not script_path:
        console.print(f"[red]ไม่พบสคริปต์ '{script}'[/red]")
        return
    
    # รันสคริปต์
    console.print(f"[green]กำลังรันสคริปต์: {script}[/green]")
    try:
        # ส่งต่อพารามิเตอร์ที่เหลือไปยังสคริปต์
        # กรอง arguments ที่ไม่จำเป็นออก (เช่น webcam.show)
        args = [arg for arg in sys.argv[3:] if arg != script]
        subprocess.run([sys.executable, script_path] + args, check=True)
    except subprocess.CalledProcessError as e:
        console.print(f"[red]เกิดข้อผิดพลาดในการรันสคริปต์: {e}[/red]")
    except Exception as e:
        console.print(f"[red]เกิดข้อผิดพลาด: {e}[/red]")

@main.command()
def list():
    """แสดงรายการสคริปต์ที่มีทั้งหมด"""
    list_available_scripts()

def find_script_path(category, script_name):
    """ค้นหาเส้นทางของสคริปต์จากชื่อหมวดหมู่และชื่อสคริปต์"""
    # ค้นหาโฟลเดอร์ scripts ในโปรเจค
    project_root = find_project_root()
    if not project_root:
        return None
    
    scripts_dir = project_root / 'scripts'
    if not scripts_dir.exists():
        return None
    
    # ค้นหาไฟล์สคริปต์
    category_dir = scripts_dir / category
    if not category_dir.exists():
        return None
    
    # ค้นหาไฟล์ที่มีชื่อตรงกับ script_name
    for file in category_dir.glob('*.py'):
        if file.stem == script_name:
            return str(file)
    
    return None

def find_project_root():
    """ค้นหาโฟลเดอร์หลักของโปรเจค"""
    current_dir = Path.cwd()
    
    # ตรวจสอบว่ามีไฟล์ pyproject.toml หรือไม่
    while current_dir != current_dir.parent:
        if (current_dir / 'pyproject.toml').exists():
            return current_dir
        current_dir = current_dir.parent
    
    return None

def list_available_scripts():
    """แสดงรายการสคริปต์ที่มีทั้งหมด"""
    project_root = find_project_root()
    if not project_root:
        console.print("[red]ไม่พบโฟลเดอร์หลักของโปรเจค[/red]")
        return
    
    scripts_dir = project_root / 'scripts'
    if not scripts_dir.exists():
        console.print("[red]ไม่พบโฟลเดอร์ scripts[/red]")
        return
    
    console.print("[bold green]รายการสคริปต์ที่มีทั้งหมด:[/bold green]")
    
    # แสดงรายการสคริปต์ในแต่ละหมวดหมู่
    for category_dir in scripts_dir.iterdir():
        if not category_dir.is_dir():
            continue
        
        category = category_dir.name
        console.print(f"\n[bold blue]{category}:[/bold blue]")
        
        # แสดงรายการสคริปต์ในหมวดหมู่
        for script_file in category_dir.glob('*.py'):
            script_name = script_file.stem
            console.print(f"  - {category}.{script_name}")
    
    console.print("\n[bold]วิธีการใช้งาน:[/bold]")
    console.print("  bmtlab run -s หมวดหมู่.ชื่อสคริปต์ [พารามิเตอร์เพิ่มเติม]")

if __name__ == "__main__":
    main()
