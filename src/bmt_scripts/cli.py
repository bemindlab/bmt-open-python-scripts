#!/usr/bin/env python3
"""
BMT Open Python Scripts - CLI
"""

import importlib.util
import os
import platform
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union

import click
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table
from rich.text import Text

# สร้าง console สำหรับการแสดงผลที่สวยงาม
console = Console()

# กำหนดค่าสีและสไตล์
STYLE_SUCCESS = "green"
STYLE_ERROR = "red"
STYLE_WARNING = "yellow"
STYLE_INFO = "blue"
STYLE_BOLD = "bold"
STYLE_HEADER = "bold cyan"


def print_header():
    """แสดงส่วนหัวของ CLI"""
    console.print(
        Panel.fit(
            "[bold cyan]BMT Open Python Scripts[/bold cyan]",
            subtitle="[italic]เครื่องมือสำหรับนักพัฒนา[/italic]",
            border_style="cyan",
        )
    )


def print_error(message: str):
    """แสดงข้อความข้อผิดพลาด"""
    console.print(f"[{STYLE_ERROR}]{message}[/{STYLE_ERROR}]")


def print_success(message: str):
    """แสดงข้อความสำเร็จ"""
    console.print(f"[{STYLE_SUCCESS}]{message}[/{STYLE_SUCCESS}]")


def print_warning(message: str):
    """แสดงข้อความเตือน"""
    console.print(f"[{STYLE_WARNING}]{message}[/{STYLE_WARNING}]")


def print_info(message: str):
    """แสดงข้อความข้อมูล"""
    console.print(f"[{STYLE_INFO}]{message}[/{STYLE_INFO}]")


def print_bold(message: str):
    """แสดงข้อความตัวหนา"""
    console.print(f"[{STYLE_BOLD}]{message}[/{STYLE_BOLD}]")


@click.group()
@click.version_option(version="0.0.1", prog_name="BMT Open Python Scripts")
def main():
    """BMT Open Python Scripts CLI"""
    print_header()


@main.command()
def version():
    """แสดงเวอร์ชันของแพ็คเกจ"""
    try:
        from bmt_scripts._version import __version__

        version_info = f"BMT Open Python Scripts เวอร์ชัน: {__version__}"
        console.print(Panel.fit(version_info, title="เวอร์ชัน", border_style="cyan"))

        # แสดงข้อมูลระบบ
        system_info = Table(
            title="ข้อมูลระบบ", show_header=True, header_style="bold magenta"
        )
        system_info.add_column("รายการ", style="cyan")
        system_info.add_column("ข้อมูล", style="green")

        system_info.add_row("Python", sys.version.split()[0])
        system_info.add_row(
            "ระบบปฏิบัติการ", f"{platform.system()} {platform.release()}"
        )
        system_info.add_row("สถาปัตยกรรม", platform.machine())

        console.print(system_info)
    except ImportError:
        print_error("ไม่สามารถโหลดข้อมูลเวอร์ชันได้")


@main.group()
def hardware():
    """เครื่องมือฮาร์ดแวร์"""
    pass


@hardware.group()
def webcam():
    """เครื่องมือเว็บแคม"""
    pass


@webcam.command(name="show")
@click.option("--camera-id", "-c", default=0, help="รหัสกล้องที่ต้องการใช้")
@click.option("--width", "-w", default=640, help="ความกว้างของภาพ")
@click.option("--height", "-h", default=480, help="ความสูงของภาพ")
def webcam_show(camera_id, width, height):
    """แสดงภาพจากกล้อง"""
    try:
        from bmt_libs.hardware.camera import Camera

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        ) as progress:
            progress.add_task(description="กำลังเริ่มต้นกล้อง...", total=None)
            time.sleep(1)  # แสดงการโหลด

        camera = Camera(camera_id=camera_id, width=width, height=height)
        print_success(f"กำลังแสดงภาพจากกล้อง ID: {camera_id}")
        print_info("กด 'q' เพื่อออก")

        camera.show_feed()
    except ImportError:
        print_error(
            "ไม่พบโมดูลที่จำเป็น กรุณาติดตั้งด้วยคำสั่ง: pip install 'bmt-scripts[hardware]'"
        )
    except Exception as e:
        print_error(f"เกิดข้อผิดพลาด: {e}")


@webcam.command(name="list")
def webcam_list():
    """แสดงรายการกล้องที่มี"""
    try:
        from bmt_libs.hardware.camera import Camera

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        ) as progress:
            progress.add_task(description="กำลังค้นหากล้อง...", total=None)
            time.sleep(1)  # แสดงการโหลด

        camera = Camera()
        cameras = camera.list_devices()

        if not cameras:
            print_warning("ไม่พบกล้อง")
            return

        # สร้างตารางแสดงรายการกล้อง
        table = Table(
            title="รายการกล้อง", show_header=True, header_style="bold magenta"
        )
        table.add_column("รหัส", style="cyan")
        table.add_column("ชื่อ", style="green")

        for idx, name in cameras.items():
            table.add_row(str(idx), name)

        console.print(table)
    except ImportError:
        print_error(
            "ไม่พบโมดูลที่จำเป็น กรุณาติดตั้งด้วยคำสั่ง: pip install 'bmt-scripts[hardware]'"
        )
    except Exception as e:
        print_error(f"เกิดข้อผิดพลาด: {e}")


@webcam.command(name="capture")
@click.option("--camera-id", "-c", default=0, help="รหัสกล้องที่ต้องการใช้")
@click.option("--output-dir", "-o", default="captures", help="ไดเรกทอรีสำหรับบันทึกภาพ")
@click.option("--filename", "-f", help="ชื่อไฟล์ (ถ้าไม่ระบุจะใช้วันที่และเวลา)")
def webcam_capture(camera_id, output_dir, filename):
    """จับภาพจากกล้อง"""
    try:
        from bmt_libs.hardware.camera import Camera

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        ) as progress:
            progress.add_task(description="กำลังเริ่มต้นกล้อง...", total=None)
            time.sleep(1)  # แสดงการโหลด

        # สร้างไดเรกทอรีถ้ายังไม่มี
        os.makedirs(output_dir, exist_ok=True)

        # กำหนดชื่อไฟล์
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"webcam_{camera_id}_{timestamp}.jpg"

        # จับภาพ
        camera = Camera(camera_id=camera_id)
        image_path = camera.capture_and_save(os.path.join(output_dir, filename))

        print_success(f"บันทึกภาพไปที่: {image_path}")
    except ImportError:
        print_error(
            "ไม่พบโมดูลที่จำเป็น กรุณาติดตั้งด้วยคำสั่ง: pip install 'bmt-scripts[hardware]'"
        )
    except Exception as e:
        print_error(f"เกิดข้อผิดพลาด: {e}")


@hardware.group()
def screen():
    """เครื่องมือจับภาพหน้าจอ"""
    pass


@screen.command(name="capture")
@click.option(
    "--output-dir", "-o", default="screen_captures", help="ไดเรกทอรีสำหรับบันทึกภาพ"
)
@click.option("--filename", "-f", help="ชื่อไฟล์ (ถ้าไม่ระบุจะใช้วันที่และเวลา)")
@click.option(
    "--region", "-r", help="พื้นที่ที่ต้องการจับภาพ (รูปแบบ: x,y,width,height)"
)
def screen_capture(output_dir, filename, region):
    """จับภาพหน้าจอ"""
    try:
        from bmt_libs.hardware.screen import Screen

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        ) as progress:
            progress.add_task(description="กำลังจับภาพหน้าจอ...", total=None)
            time.sleep(1)  # แสดงการโหลด

        # สร้างไดเรกทอรีถ้ายังไม่มี
        os.makedirs(output_dir, exist_ok=True)

        # กำหนดชื่อไฟล์
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"screen_{timestamp}.png"

        # จับภาพหน้าจอ
        screen = Screen()

        # ตรวจสอบว่ามีการระบุพื้นที่หรือไม่
        if region:
            try:
                x, y, width, height = map(int, region.split(","))
                image_path = screen.capture_region(
                    x, y, width, height, os.path.join(output_dir, filename)
                )
            except ValueError:
                print_error(
                    "รูปแบบพื้นที่ไม่ถูกต้อง กรุณาระบุในรูปแบบ: x,y,width,height"
                )
                return
        else:
            image_path = screen.capture_and_save(os.path.join(output_dir, filename))

        print_success(f"บันทึกภาพไปที่: {image_path}")
    except ImportError:
        print_error(
            "ไม่พบโมดูลที่จำเป็น กรุณาติดตั้งด้วยคำสั่ง: pip install 'bmt-scripts[hardware]'"
        )
    except Exception as e:
        print_error(f"เกิดข้อผิดพลาด: {e}")


@screen.command(name="info")
def screen_info():
    """แสดงข้อมูลหน้าจอ"""
    try:
        from bmt_libs.hardware.screen import Screen

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        ) as progress:
            progress.add_task(description="กำลังค้นหาข้อมูลหน้าจอ...", total=None)
            time.sleep(1)  # แสดงการโหลด

        screen = Screen()
        screens = screen.list_screens()

        if not screens:
            print_warning("ไม่พบหน้าจอ")
            return

        # สร้างตารางแสดงข้อมูลหน้าจอ
        table = Table(
            title="ข้อมูลหน้าจอ", show_header=True, header_style="bold magenta"
        )
        table.add_column("รหัส", style="cyan")
        table.add_column("ความละเอียด", style="green")
        table.add_column("ความกว้าง", style="blue")
        table.add_column("ความสูง", style="blue")

        for idx, screen_info in enumerate(screens):
            table.add_row(
                str(idx),
                screen_info.get("resolution", "N/A"),
                str(screen_info.get("width", "N/A")),
                str(screen_info.get("height", "N/A")),
            )

        console.print(table)
    except ImportError:
        print_error(
            "ไม่พบโมดูลที่จำเป็น กรุณาติดตั้งด้วยคำสั่ง: pip install 'bmt-scripts[hardware]'"
        )
    except Exception as e:
        print_error(f"เกิดข้อผิดพลาด: {e}")


@main.group()
def git():
    """เครื่องมือ Git"""
    pass


@git.command(name="commit-summary")
@click.option("--repo-path", "-r", default=".", help="เส้นทางไปยัง Git repository")
@click.option("--days", "-d", default=7, help="จำนวนวันย้อนหลังที่ต้องการสรุป")
@click.option("--author", "-a", help="กรองตามผู้เขียน")
def git_commit_summary(repo_path, days, author):
    """สร้างสรุปการ commit ของ Git"""
    try:
        from bmt_libs.git.summary import generate_commit_summary

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        ) as progress:
            progress.add_task(
                description="กำลังวิเคราะห์ Git repository...", total=None
            )
            time.sleep(1)  # แสดงการโหลด

        # สร้างสรุป
        summary = generate_commit_summary(repo_path, days=days, author=author)

        # แสดงผลลัพธ์
        console.print(Panel.fit(summary, title="สรุปการ Commit", border_style="cyan"))
    except ImportError:
        print_error(
            "ไม่พบโมดูลที่จำเป็น กรุณาติดตั้งด้วยคำสั่ง: pip install 'bmt-scripts[dev]'"
        )
    except Exception as e:
        print_error(f"เกิดข้อผิดพลาด: {e}")


@main.group()
def agents():
    """เครื่องมือ AI agent"""
    pass


@agents.command(name="mockup")
@click.option("--prompt", "-p", required=True, help="คำอธิบายสำหรับสร้าง mockup")
@click.option(
    "--output-dir", "-o", default="mockups", help="ไดเรกทอรีสำหรับบันทึก mockup"
)
def agents_mockup(prompt, output_dir):
    """สร้าง mockup ด้วย AI"""
    try:
        from bmt_libs.agents.mockup import generate_mockup

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        ) as progress:
            progress.add_task(description="กำลังสร้าง mockup...", total=None)
            time.sleep(1)  # แสดงการโหลด

        # สร้างไดเรกทอรีถ้ายังไม่มี
        os.makedirs(output_dir, exist_ok=True)

        # สร้าง mockup
        result = generate_mockup(prompt, output_dir)

        print_success(f"สร้าง mockup สำเร็จ: {result}")
    except ImportError:
        print_error(
            "ไม่พบโมดูลที่จำเป็น กรุณาติดตั้งด้วยคำสั่ง: pip install 'bmt-scripts[agents]'"
        )
    except Exception as e:
        print_error(f"เกิดข้อผิดพลาด: {e}")


@agents.group(name="autogen")
def agents_autogen():
    """เครื่องมือ AutoGen agent"""
    pass


@agents_autogen.command(name="code")
@click.option("--prompt", "-p", required=True, help="คำอธิบายงานโค้ด")
@click.option("--output-file", "-o", help="ไฟล์สำหรับบันทึกโค้ด")
def autogen_code(prompt, output_file):
    """ใช้ code agent เพื่อสร้างหรือแก้ไขโค้ด"""
    try:
        from bmt_libs.agents.autogen.core import CodeAgent

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        ) as progress:
            progress.add_task(description="กำลังเริ่มต้น code agent...", total=None)
            time.sleep(1)  # แสดงการโหลด

        agent = CodeAgent()

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        ) as progress:
            progress.add_task(description="กำลังประมวลผลคำขอ...", total=None)
            time.sleep(1)  # แสดงการโหลด

        result = agent.write_code(prompt)

        # บันทึกผลลัพธ์ลงไฟล์ถ้ามีการระบุ
        if output_file:
            with open(output_file, "w") as f:
                f.write(result)
            print_success(f"บันทึกโค้ดไปที่: {output_file}")

        # แสดงผลลัพธ์
        console.print(Panel.fit(result, title="โค้ดที่สร้าง", border_style="cyan"))
    except ImportError:
        print_error(
            "ไม่พบโมดูลที่จำเป็น กรุณาติดตั้งด้วยคำสั่ง: pip install 'bmt-scripts[agents]'"
        )
    except Exception as e:
        print_error(f"เกิดข้อผิดพลาด: {e}")


@agents_autogen.command(name="research")
@click.option("--topic", "-t", required=True, help="หัวข้อการวิจัย")
@click.option("--output-file", "-o", help="ไฟล์สำหรับบันทึกผลการวิจัย")
def autogen_research(topic, output_file):
    """ใช้ research agent เพื่อรวบรวมข้อมูลเกี่ยวกับหัวข้อ"""
    try:
        from bmt_libs.agents.autogen.core import ResearchAgent

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        ) as progress:
            progress.add_task(description="กำลังเริ่มต้น research agent...", total=None)
            time.sleep(1)  # แสดงการโหลด

        agent = ResearchAgent()

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        ) as progress:
            progress.add_task(description="กำลังวิจัยหัวข้อของคุณ...", total=None)
            time.sleep(1)  # แสดงการโหลด

        result = agent.research(topic)

        # บันทึกผลลัพธ์ลงไฟล์ถ้ามีการระบุ
        if output_file:
            with open(output_file, "w") as f:
                f.write(result)
            print_success(f"บันทึกผลการวิจัยไปที่: {output_file}")

        # แสดงผลลัพธ์
        console.print(Panel.fit(result, title="ผลการวิจัย", border_style="cyan"))
    except ImportError:
        print_error(
            "ไม่พบโมดูลที่จำเป็น กรุณาติดตั้งด้วยคำสั่ง: pip install 'bmt-scripts[agents]'"
        )
    except Exception as e:
        print_error(f"เกิดข้อผิดพลาด: {e}")


@agents_autogen.command(name="creative")
@click.option("--topic", "-t", required=True, help="หัวข้อเนื้อหาสร้างสรรค์")
@click.option(
    "--type",
    "-y",
    default="article",
    type=click.Choice(["article", "script", "ideas"]),
    help="ประเภทของเนื้อหาที่ต้องการสร้าง",
)
@click.option("--output-file", "-o", help="ไฟล์สำหรับบันทึกเนื้อหา")
def autogen_creative(topic, type, output_file):
    """ใช้ creative agent เพื่อสร้างเนื้อหา"""
    try:
        from bmt_libs.agents.autogen.core import CreativeAgent

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        ) as progress:
            progress.add_task(description="กำลังเริ่มต้น creative agent...", total=None)
            time.sleep(1)  # แสดงการโหลด

        agent = CreativeAgent()

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        ) as progress:
            progress.add_task(description=f"กำลังสร้างเนื้อหา{type}...", total=None)
            time.sleep(1)  # แสดงการโหลด

        # สร้างเนื้อหาตามประเภท
        if type == "article":
            result = agent.write_article(topic)
        elif type == "script":
            result = agent.write_script(topic)
        elif type == "ideas":
            result = agent.generate_ideas(topic)

        # บันทึกผลลัพธ์ลงไฟล์ถ้ามีการระบุ
        if output_file:
            with open(output_file, "w") as f:
                f.write(result)
            print_success(f"บันทึกเนื้อหาไปที่: {output_file}")

        # แสดงผลลัพธ์
        console.print(
            Panel.fit(result, title=f"เนื้อหา{type}ที่สร้าง", border_style="cyan")
        )
    except ImportError:
        print_error(
            "ไม่พบโมดูลที่จำเป็น กรุณาติดตั้งด้วยคำสั่ง: pip install 'bmt-scripts[agents]'"
        )
    except Exception as e:
        print_error(f"เกิดข้อผิดพลาด: {e}")


@main.command()
@click.option(
    "--script",
    "-s",
    help="ชื่อสคริปต์ที่ต้องการรัน (เช่น webcam.show, git.commit-summary)",
)
def run(script):
    """รันสคริปต์ที่เลือก (คำสั่งเก่าสำหรับความเข้ากันได้ย้อนหลัง)"""
    if not script:
        # แสดงสคริปต์ทั้งหมดที่มี
        list_available_scripts()
        return

    # แยกหมวดหมู่และชื่อสคริปต์
    parts = script.split(".")
    if len(parts) != 2:
        print_error(
            "รูปแบบชื่อสคริปต์ไม่ถูกต้อง กรุณาระบุในรูปแบบ 'category.script-name'"
        )
        return

    category, script_name = parts

    # ตรวจสอบว่าสคริปต์มีอยู่หรือไม่
    script_path = find_script_path(category, script_name)
    if not script_path:
        print_error(f"ไม่พบสคริปต์ '{script}'")
        return

    # รันสคริปต์
    print_info(f"กำลังรันสคริปต์: {script}")
    try:
        # ส่งพารามิเตอร์ที่เหลือไปยังสคริปต์
        # กรองอาร์กิวเมนต์ที่ไม่จำเป็น (เช่น webcam.show)
        args = [arg for arg in sys.argv[3:] if arg != script]

        # ตั้งค่า PYTHONPATH เพื่อรวมโฟลเดอร์รูทของโปรเจค
        project_root = find_project_root()
        if project_root:
            env = os.environ.copy()
            # เพิ่มโฟลเดอร์ src ใน PYTHONPATH
            src_path = str(project_root / "src")
            if "PYTHONPATH" in env:
                env["PYTHONPATH"] = f"{src_path}:{env['PYTHONPATH']}"
            else:
                env["PYTHONPATH"] = src_path

            # รันสคริปต์ด้วย PYTHONPATH ที่กำหนด
            subprocess.run([sys.executable, script_path] + args, check=True, env=env)
        else:
            # ถ้าไม่พบโฟลเดอร์รูทของโปรเจค รันสคริปต์ตามปกติ
            subprocess.run([sys.executable, script_path] + args, check=True)
    except subprocess.CalledProcessError as e:
        print_error(f"เกิดข้อผิดพลาดในการรันสคริปต์: {e}")
    except Exception as e:
        print_error(f"เกิดข้อผิดพลาด: {e}")


@main.command()
def list():
    """แสดงรายการสคริปต์ทั้งหมดที่มี"""
    list_available_scripts()


@main.command()
def check_dependencies():
    """ตรวจสอบการติดตั้งแพ็คเกจที่จำเป็น"""
    try:
        import pkg_resources  # type: ignore

        # ตรวจสอบแพ็คเกจหลัก
        required_packages = ["opencv-python", "numpy", "rich", "click", "python-dotenv"]

        # ตรวจสอบแพ็คเกจเสริม
        optional_packages = {
            "agents": ["pyautogen"],
            "hardware": ["pyautogui"],
            "dev": ["pytest", "black", "isort", "mypy", "bandit"],
        }

        # สร้างตารางแสดงผล
        table = Table(
            title="สถานะการติดตั้งแพ็คเกจ",
            show_header=True,
            header_style="bold magenta",
        )
        table.add_column("แพ็คเกจ", style="cyan")
        table.add_column("เวอร์ชัน", style="green")
        table.add_column("สถานะ", style="blue")

        # ตรวจสอบแพ็คเกจหลัก
        for package in required_packages:
            try:
                version = pkg_resources.get_distribution(package).version
                table.add_row(package, version, "✅ ติดตั้งแล้ว")
            except pkg_resources.DistributionNotFound:
                table.add_row(package, "N/A", "❌ ไม่พบ")

        # ตรวจสอบแพ็คเกจเสริม
        for group, packages in optional_packages.items():
            for package in packages:
                try:
                    version = pkg_resources.get_distribution(package).version
                    table.add_row(f"{package} ({group})", version, "✅ ติดตั้งแล้ว")
                except pkg_resources.DistributionNotFound:
                    table.add_row(f"{package} ({group})", "N/A", "❌ ไม่พบ")

        console.print(table)

        # แสดงคำแนะนำ
        print_info("คำแนะนำ:")
        print_info("  - ถ้าต้องการใช้ฟีเจอร์ agents: pip install 'bmt-scripts[agents]'")
        print_info(
            "  - ถ้าต้องการใช้ฟีเจอร์ hardware: pip install 'bmt-scripts[hardware]'"
        )
        print_info("  - ถ้าต้องการใช้ฟีเจอร์ dev: pip install 'bmt-scripts[dev]'")
        print_info("  - ถ้าต้องการใช้ทุกฟีเจอร์: pip install 'bmt-scripts[all]'")
    except Exception as e:
        print_error(f"เกิดข้อผิดพลาด: {e}")


def find_script_path(category, script_name):
    """ค้นหาเส้นทางของสคริปต์จากหมวดหมู่และชื่อสคริปต์"""
    # ค้นหาโฟลเดอร์สคริปต์ในโปรเจค
    project_root = find_project_root()
    if not project_root:
        return None

    # ตรวจสอบว่ามีโฟลเดอร์ src/bmt_scripts หรือไม่
    src_dir = project_root / "src" / "bmt_scripts"
    if not src_dir.exists():
        return None

    # ค้นหาไฟล์สคริปต์ในโฟลเดอร์ที่เกี่ยวข้อง
    category_dir = None

    # ตรวจสอบโฟลเดอร์ที่มีอยู่
    if category == "webcam" and (src_dir / "webcam").exists():
        category_dir = src_dir / "webcam"
    elif category == "hardware" and (src_dir / "hardware").exists():
        category_dir = src_dir / "hardware"
    elif category == "git" and (src_dir / "git").exists():
        category_dir = src_dir / "git"
    elif category == "agents" and (src_dir / "agents").exists():
        category_dir = src_dir / "agents"
    elif category == "plugins" and (src_dir / "plugins").exists():
        category_dir = src_dir / "plugins"

    if not category_dir:
        return None

    # ค้นหาไฟล์ที่ตรงกับชื่อสคริปต์
    for file in category_dir.glob("*.py"):
        if file.stem == script_name:
            return str(file)

    return None


def find_project_root():
    """ค้นหาโฟลเดอร์รูทของโปรเจค"""
    current_dir = Path.cwd()

    # ตรวจสอบว่ามีไฟล์ pyproject.toml หรือไม่
    while current_dir != current_dir.parent:
        if (current_dir / "pyproject.toml").exists():
            return current_dir
        current_dir = current_dir.parent

    return None


def list_available_scripts():
    """แสดงรายการสคริปต์ทั้งหมดที่มี"""
    project_root = find_project_root()
    if not project_root:
        print_error("ไม่พบโฟลเดอร์รูทของโปรเจค")
        return

    src_dir = project_root / "src" / "bmt_scripts"
    if not src_dir.exists():
        print_error("ไม่พบโฟลเดอร์ src/bmt_scripts")
        return

    print_bold("สคริปต์ที่มีทั้งหมด:")

    # สร้างตารางแสดงรายการสคริปต์
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("หมวดหมู่", style="cyan")
    table.add_column("สคริปต์", style="green")
    table.add_column("คำอธิบาย", style="blue")

    # ตรวจสอบโฟลเดอร์ที่มีอยู่
    categories = {
        "webcam": src_dir / "webcam",
        "hardware": src_dir / "hardware",
        "git": src_dir / "git",
        "agents": src_dir / "agents",
        "plugins": src_dir / "plugins",
    }

    # แสดงรายการสคริปต์ในแต่ละหมวดหมู่
    for category_name, category_dir in categories.items():
        if not category_dir.exists():
            continue

        # แสดงรายการสคริปต์ในหมวดหมู่
        for script_file in category_dir.glob("*.py"):
            if script_file.name == "__init__.py":
                continue

            script_name = script_file.stem

            # อ่านคำอธิบายสคริปต์จาก docstring
            description = "ไม่มีคำอธิบาย"
            try:
                with open(script_file, encoding="utf-8") as f:
                    content = f.read()
                    if '"""' in content:
                        docstring = content.split('"""')[1].strip()
                        if docstring:
                            description = docstring.split("\n")[0]
            except:
                pass

            table.add_row(category_name, script_name, description)

    console.print(table)

    print_bold("\nวิธีการใช้งาน:")
    print_info("  bmtlab run -s category.script-name [พารามิเตอร์เพิ่มเติม]")
    print_info("  หรือใช้รูปแบบคำสั่งใหม่:")
    print_info("  bmtlab category script-name [พารามิเตอร์]")


if __name__ == "__main__":
    main()
