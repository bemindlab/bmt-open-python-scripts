#!/usr/bin/env python3
"""
ตัวอย่างการใช้งาน AutoGen Group Chat

สคริปต์นี้แสดงตัวอย่างการใช้งาน AutoGen ในการทำงานร่วมกันระหว่าง agents หลายตัว
"""

import os
import sys
from typing import Any, Dict

# เพิ่มโฟลเดอร์หลักของโปรเจคเข้าไปใน Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from lib.agents.autogen import CodeAgent, CreativeAgent, ResearchAgent  # noqa: E402


def main() -> None:
    """ฟังก์ชันหลัก"""
    # ตรวจสอบ API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("กรุณาตั้งค่า OPENAI_API_KEY ในตัวแปรสภาพแวดล้อม")
        return

    # สร้าง agents
    code_agent = CodeAgent(api_key=api_key)
    research_agent = ResearchAgent(api_key=api_key)
    creative_agent = CreativeAgent(api_key=api_key)

    # ตัวอย่างการทำงานร่วมกันระหว่าง agents
    print("\n=== ตัวอย่างการทำงานร่วมกันระหว่าง agents ===")

    # สร้าง group chat
    group_chat = code_agent.create_group_chat(
        agents=[research_agent.agent, creative_agent.agent],
        group_name="project_planning",
    )

    # กำหนดหัวข้อสำหรับ group chat
    topic = """
    เราต้องการพัฒนาแอปพลิเคชัน Python สำหรับการจัดการงาน (Task Management)
    กรุณาช่วยวางแผนการพัฒนาแอปพลิเคชันนี้ โดยพิจารณาถึง:
    1. คุณสมบัติหลักของแอปพลิเคชัน
    2. เทคโนโลยีที่ควรใช้
    3. โครงสร้างโค้ดเบื้องต้น
    4. แนวทางการทดสอบ
    """

    # เริ่ม group chat
    print(f"หัวข้อ: {topic}")
    print("\nกำลังเริ่ม group chat...")

    result = code_agent.run_group_chat(group_chat, topic)

    print("\nผลลัพธ์ของ group chat:")
    print(result["summary"])

    # ตัวอย่างการทำงานร่วมกันระหว่าง agents ในการแก้ไขปัญหา
    print("\n=== ตัวอย่างการทำงานร่วมกันในการแก้ไขปัญหา ===")

    # สร้าง group chat ใหม่
    problem_solving_chat = code_agent.create_group_chat(
        agents=[research_agent.agent, creative_agent.agent],
        group_name="problem_solving",
    )

    # กำหนดปัญหาสำหรับ group chat
    problem = """
    เรามีโค้ด Python ต่อไปนี้ที่มีปัญหา:

    ```python
    def process_user_data(user_data):
        result = {}
        for key, value in user_data.items():
            if isinstance(value, str):
                result[key] = value.upper()
            elif isinstance(value, (int, float)):
                result[key] = value * 2
            else:
                result[key] = value
        return result

    # ข้อมูลตัวอย่าง
    user_data = {
        "name": "John Doe",
        "age": 30,
        "email": "john@example.com",
        "scores": [85, 90, 95],
        "active": True
    }

    # การใช้งาน
    processed_data = process_user_data(user_data)
    print(processed_data)
    ```

    ปัญหาคือ:
    1. โค้ดไม่สามารถประมวลผลข้อมูลที่เป็นรายการ (list) ได้
    2. โค้ดไม่มีการจัดการข้อผิดพลาด (error handling)
    3. โค้ดไม่มีการตรวจสอบความถูกต้องของข้อมูล (data validation)

    กรุณาช่วยแก้ไขปัญหาเหล่านี้
    """

    # เริ่ม group chat
    print(f"ปัญหา: {problem}")
    print("\nกำลังเริ่ม group chat...")

    problem_result = code_agent.run_group_chat(problem_solving_chat, problem)

    print("\nผลลัพธ์ของ group chat:")
    print(problem_result["summary"])

    # ตัวอย่างการทำงานร่วมกันระหว่าง agents ในการสร้างสรรค์เนื้อหา
    print("\n=== ตัวอย่างการทำงานร่วมกันในการสร้างสรรค์เนื้อหา ===")

    # สร้าง group chat ใหม่
    content_creation_chat = creative_agent.create_group_chat(
        agents=[research_agent.agent, code_agent.agent], group_name="content_creation"
    )

    # กำหนดหัวข้อสำหรับ group chat
    content_topic = """
    เราต้องการสร้างเว็บไซต์บล็อกเกี่ยวกับเทคโนโลยี
    กรุณาช่วยวางแผนเนื้อหาและโครงสร้างของเว็บไซต์ โดยพิจารณาถึง:
    1. หัวข้อบทความที่น่าสนใจ
    2. โครงสร้างของเว็บไซต์
    3. เทคโนโลยีที่ควรใช้ในการพัฒนา
    4. แนวทางการโปรโมทเว็บไซต์
    """

    # เริ่ม group chat
    print(f"หัวข้อ: {content_topic}")
    print("\nกำลังเริ่ม group chat...")

    content_result = creative_agent.run_group_chat(content_creation_chat, content_topic)

    print("\nผลลัพธ์ของ group chat:")
    print(content_result["summary"])


if __name__ == "__main__":
    main()
