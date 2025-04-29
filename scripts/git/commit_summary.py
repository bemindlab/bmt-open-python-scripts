#!/usr/bin/env python3
import datetime
import os
import subprocess
import sys
from typing import Any, Dict, List


class CommitInfo:
    def __init__(self, hash: str, author: str, date: str, message: str):
        self.hash = hash
        self.author = author
        self.date = date
        self.message = message


def is_git_repository() -> bool:
    """ตรวจสอบว่าอยู่ใน git repository หรือไม่"""
    try:
        subprocess.check_output(
            ["git", "rev-parse", "--is-inside-work-tree"], stderr=subprocess.STDOUT
        )
        return True
    except subprocess.CalledProcessError:
        return False


def has_commits() -> bool:
    """ตรวจสอบว่ามี commit ใน repository หรือไม่"""
    try:
        subprocess.check_output(["git", "rev-parse", "HEAD"], stderr=subprocess.STDOUT)
        return True
    except subprocess.CalledProcessError:
        return False


def get_current_commit() -> CommitInfo:
    """ดึงข้อมูล commit ล่าสุด"""
    if not is_git_repository():
        raise Exception("ไม่พบ git repository ในไดเรกทอรีปัจจุบัน")

    if not has_commits():
        raise Exception("ไม่พบ commit ใน repository นี้ กรุณาทำการ commit ก่อน")

    hash = subprocess.check_output(["git", "rev-parse", "HEAD"]).decode().strip()
    author = (
        subprocess.check_output(["git", "log", "-1", "--pretty=format:%an"])
        .decode()
        .strip()
    )
    date = (
        subprocess.check_output(["git", "log", "-1", "--pretty=format:%ad"])
        .decode()
        .strip()
    )
    message = (
        subprocess.check_output(["git", "log", "-1", "--pretty=format:%B"])
        .decode()
        .strip()
    )

    return CommitInfo(hash, author, date, message)


def get_changed_files() -> List[str]:
    """ดึงรายการไฟล์ที่เปลี่ยนแปลงใน staging area"""
    try:
        output = (
            subprocess.check_output(["git", "diff", "--cached", "--name-only"])
            .decode()
            .strip()
        )
        return output.split("\n") if output else []
    except subprocess.CalledProcessError:
        return []


def generate_prompt(commit_info: CommitInfo, changed_files: List[str]) -> str:
    """สร้างข้อความ prompt สำหรับ AI"""
    return f"""กรุณาสร้างสรุปรายละเอียดของ commit ต่อไปนี้:

Commit Hash: {commit_info.hash}
Author: {commit_info.author}
Date: {commit_info.date}
Message: {commit_info.message}

ไฟล์ที่เปลี่ยนแปลง:
{chr(10).join([f"- {file}" for file in changed_files])}

กรุณาให้ข้อมูลดังนี้:
1. สรุปการเปลี่ยนแปลงอย่างกระชับ
2. การแก้ไขที่สำคัญในแต่ละไฟล์
3. ผลกระทบที่อาจเกิดขึ้นจากการเปลี่ยนแปลงเหล่านี้
4. การเปลี่ยนแปลงที่อาจทำให้เกิดปัญหา (breaking changes) หรือหมายเหตุสำคัญ"""


def save_summary(
    summary: str, commit_info: CommitInfo, changed_files: List[str]
) -> str:
    """บันทึกสรุปการ commit ลงในไฟล์"""
    summary_dir = os.path.join(os.getcwd(), "__dev_logs__", "commit_summaries")
    os.makedirs(summary_dir, exist_ok=True)

    filename = f"{datetime.datetime.now().strftime('%Y-%m-%d')}_{commit_info.hash}.md"
    filepath = os.path.join(summary_dir, filename)

    content = f"""# สรุปการ Commit

## รายละเอียด Commit
- **Hash:** {commit_info.hash}
- **ผู้เขียน:** {commit_info.author}
- **วันที่:** {commit_info.date}
- **ข้อความ:** {commit_info.message}

## สรุปที่สร้างโดย AI
{summary}

## ไฟล์ที่เปลี่ยนแปลง
{chr(10).join([f"- {file}" for file in changed_files])}
"""

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"บันทึกสรุปไปที่: {filepath}")
    return filepath


def main():
    try:
        if not is_git_repository():
            print("ข้อผิดพลาด: ไม่พบ git repository ในไดเรกทอรีปัจจุบัน")
            sys.exit(1)

        if not has_commits():
            print("ข้อผิดพลาด: ไม่พบ commit ใน repository นี้ กรุณาทำการ commit ก่อน")
            sys.exit(1)

        commit_info = get_current_commit()
        changed_files = get_changed_files()

        print(f"กำลังสร้างสรุปการ commit {commit_info.hash} ...")
        print("หมายเหตุ: กรุณาใช้ Cursor AI เพื่อวิเคราะห์คำขอต่อไปนี้:")
        print("\n" + generate_prompt(commit_info, changed_files))
        print("\nหลังจากได้รับสรุปจาก Cursor AI แล้ว กรุณาบันทึกเพื่อดำเนินการต่อ")

        print("\nกด Enter หลังจากที่คุณได้รับสรุปจาก Cursor AI แล้ว...")
        input()

        print("กรุณาวางสรุปจาก Cursor AI (กด Ctrl+D เมื่อเสร็จสิ้น):")

        # รับข้อมูลจากผู้ใช้
        summary_lines = []
        try:
            while True:
                line = input()
                summary_lines.append(line)
        except EOFError:
            pass

        summary = "\n".join(summary_lines).strip()

        # บันทึก summary และรับค่า filepath
        filepath = save_summary(summary, commit_info, changed_files)

        print("สรุปการ commit ถูกบันทึกไปที่: ", filepath)

    except subprocess.CalledProcessError as e:
        print(f"ข้อผิดพลาด: {e}")
        sys.exit(1)

    except Exception as e:
        print(f"ข้อผิดพลาด: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
