#!/usr/bin/env python3
"""
ตัวอย่างการใช้งาน AutoGen

สคริปต์นี้แสดงตัวอย่างการใช้งาน AutoGen ผ่าน core feature library
"""

import os
import sys
from typing import Dict, Any

# เพิ่มโฟลเดอร์หลักของโปรเจคเข้าไปใน Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from lib.agents.autogen import CodeAgent, ResearchAgent, CreativeAgent


def main():
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
    
    # ตัวอย่างการใช้งาน CodeAgent
    print("\n=== ตัวอย่างการใช้งาน CodeAgent ===")
    code_description = "เขียนฟังก์ชัน Python สำหรับคำนวณค่าเฉลี่ยของรายการตัวเลข"
    code_result = code_agent.write_code(code_description)
    print(f"คำอธิบาย: {code_description}")
    print(f"โค้ดที่ได้:\n{code_result}")
    
    # ตัวอย่างการแก้ไขบั๊ก
    buggy_code = """
def calculate_average(numbers):
    total = 0
    for num in numbers:
        total += num
    return total / len(numbers)  # อาจเกิด ZeroDivisionError ถ้า numbers เป็นรายการว่าง
"""
    error_message = "ZeroDivisionError: division by zero"
    fixed_code = code_agent.fix_bug(buggy_code, error_message)
    print("\nโค้ดที่มีบั๊ก:")
    print(buggy_code)
    print(f"โค้ดที่แก้ไขแล้ว:\n{fixed_code}")
    
    # ตัวอย่างการปรับปรุงโค้ด
    code_to_refactor = """
def process_data(data):
    result = []
    for item in data:
        if item > 0:
            result.append(item * 2)
    return result
"""
    refactored_code = code_agent.refactor_code(code_to_refactor)
    print("\nโค้ดก่อนปรับปรุง:")
    print(code_to_refactor)
    print(f"โค้ดหลังปรับปรุง:\n{refactored_code}")
    
    # ตัวอย่างการใช้งาน ResearchAgent
    print("\n=== ตัวอย่างการใช้งาน ResearchAgent ===")
    research_topic = "ประโยชน์ของ Python ในการพัฒนาเว็บแอปพลิเคชัน"
    research_result = research_agent.research(research_topic)
    print(f"หัวข้อ: {research_topic}")
    print(f"ผลการค้นคว้า:\n{research_result}")
    
    # ตัวอย่างการวิเคราะห์ข้อมูล
    data_to_analyze = """
    ข้อมูลการใช้งาน Python ในปี 2023:
    - 48% ของนักพัฒนามืออาชีพใช้ Python
    - Python เป็นภาษาที่มีผู้ใช้มากที่สุดเป็นอันดับ 1
    - 27% ของโปรเจคใหม่ใช้ Python
    - 35% ของนักพัฒนาที่ใช้ Python เป็นนักพัฒนามืออาชีพมากกว่า 5 ปี
    """
    analysis_result = research_agent.analyze_data(data_to_analyze)
    print("\nข้อมูลที่วิเคราะห์:")
    print(data_to_analyze)
    print(f"ผลการวิเคราะห์:\n{analysis_result}")
    
    # ตัวอย่างการใช้งาน CreativeAgent
    print("\n=== ตัวอย่างการใช้งาน CreativeAgent ===")
    article_topic = "อนาคตของปัญญาประดิษฐ์ในประเทศไทย"
    article_result = creative_agent.write_article(article_topic, length="short")
    print(f"หัวข้อ: {article_topic}")
    print(f"บทความ:\n{article_result}")
    
    # ตัวอย่างการสร้างไอเดีย
    idea_topic = "แอปพลิเคชันเพื่อสุขภาพ"
    ideas_result = creative_agent.generate_ideas(idea_topic, count=3)
    print(f"\nหัวข้อ: {idea_topic}")
    print(f"ไอเดีย:\n{ideas_result}")


if __name__ == "__main__":
    main() 