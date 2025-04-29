#!/usr/bin/env python3
"""
ตัวอย่างการใช้งาน AutoGen ในการทำงานกับไฟล์และข้อมูล

สคริปต์นี้แสดงตัวอย่างการใช้งาน AutoGen ในการทำงานกับไฟล์และข้อมูล
"""

import os
import sys
import json
import csv
from typing import Dict, Any, List

# เพิ่มโฟลเดอร์หลักของโปรเจคเข้าไปใน Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from lib.agents.autogen import CodeAgent, ResearchAgent


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
    
    # ตัวอย่างการสร้างไฟล์ JSON
    print("\n=== ตัวอย่างการสร้างไฟล์ JSON ===")
    
    # สร้างข้อมูล JSON
    json_data = {
        "users": [
            {"id": 1, "name": "John Doe", "email": "john@example.com", "active": True},
            {"id": 2, "name": "Jane Smith", "email": "jane@example.com", "active": True},
            {"id": 3, "name": "Bob Johnson", "email": "bob@example.com", "active": False},
        ],
        "settings": {
            "theme": "dark",
            "language": "th",
            "notifications": True,
        },
    }
    
    # บันทึกข้อมูลลงในไฟล์ JSON
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(json_data, f, ensure_ascii=False, indent=4)
    
    print("บันทึกข้อมูลลงในไฟล์ data.json แล้ว")
    
    # อ่านข้อมูลจากไฟล์ JSON
    with open("data.json", "r", encoding="utf-8") as f:
        loaded_data = json.load(f)
    
    print("ข้อมูลที่อ่านได้:")
    print(json.dumps(loaded_data, ensure_ascii=False, indent=2))
    
    # ตัวอย่างการสร้างไฟล์ CSV
    print("\n=== ตัวอย่างการสร้างไฟล์ CSV ===")
    
    # สร้างข้อมูล CSV
    csv_data = [
        ["id", "name", "email", "active"],
        [1, "John Doe", "john@example.com", True],
        [2, "Jane Smith", "jane@example.com", True],
        [3, "Bob Johnson", "bob@example.com", False],
    ]
    
    # บันทึกข้อมูลลงในไฟล์ CSV
    with open("data.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(csv_data)
    
    print("บันทึกข้อมูลลงในไฟล์ data.csv แล้ว")
    
    # อ่านข้อมูลจากไฟล์ CSV
    with open("data.csv", "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        loaded_csv_data = list(reader)
    
    print("ข้อมูลที่อ่านได้:")
    for row in loaded_csv_data:
        print(row)
    
    # ตัวอย่างการใช้งาน AutoGen ในการวิเคราะห์ข้อมูล
    print("\n=== ตัวอย่างการใช้งาน AutoGen ในการวิเคราะห์ข้อมูล ===")
    
    # แปลงข้อมูล CSV เป็น JSON
    csv_to_json = []
    headers = loaded_csv_data[0]
    
    for row in loaded_csv_data[1:]:
        item = {}
        for i, value in enumerate(row):
            # แปลงค่า boolean
            if value.lower() == "true":
                value = True
            elif value.lower() == "false":
                value = False
            # แปลงค่า integer
            elif value.isdigit():
                value = int(value)
            
            item[headers[i]] = value
        
        csv_to_json.append(item)
    
    # บันทึกข้อมูลที่แปลงแล้วลงในไฟล์ JSON
    with open("csv_to_json.json", "w", encoding="utf-8") as f:
        json.dump({"users": csv_to_json}, f, ensure_ascii=False, indent=4)
    
    print("แปลงข้อมูล CSV เป็น JSON และบันทึกลงในไฟล์ csv_to_json.json แล้ว")
    
    # วิเคราะห์ข้อมูลโดยใช้ ResearchAgent
    data_to_analyze = json.dumps(csv_to_json, ensure_ascii=False, indent=2)
    analysis_result = research_agent.analyze_data(data_to_analyze)
    
    print("\nผลการวิเคราะห์ข้อมูล:")
    print(analysis_result)
    
    # ตัวอย่างการใช้งาน AutoGen ในการสร้างโค้ดสำหรับการทำงานกับไฟล์
    print("\n=== ตัวอย่างการใช้งาน AutoGen ในการสร้างโค้ดสำหรับการทำงานกับไฟล์ ===")
    
    # สร้างโค้ดสำหรับการอ่านไฟล์ CSV และแปลงเป็น JSON
    code_description = """
    เขียนฟังก์ชัน Python สำหรับการอ่านไฟล์ CSV และแปลงเป็น JSON
    ฟังก์ชันควรมีพารามิเตอร์ดังนี้:
    - file_path: เส้นทางของไฟล์ CSV
    - output_file: เส้นทางของไฟล์ JSON ที่ต้องการบันทึก (ถ้าไม่ระบุจะไม่บันทึก)
    
    ฟังก์ชันควรส่งคืนข้อมูลในรูปแบบ JSON
    """
    
    code_result = code_agent.write_code(code_description)
    
    print("คำอธิบาย:")
    print(code_description)
    print("\nโค้ดที่ได้:")
    print(code_result)
    
    # ตัวอย่างการใช้งาน AutoGen ในการแก้ไขโค้ด
    print("\n=== ตัวอย่างการใช้งาน AutoGen ในการแก้ไขโค้ด ===")
    
    # โค้ดที่มีบั๊ก
    buggy_code = """
def read_csv_to_json(file_path, output_file=None):
    import csv
    import json
    
    data = []
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        headers = next(reader)  # อ่านส่วนหัว
    
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append(row)
    
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    
    return data
"""
    
    # ข้อความแสดงข้อผิดพลาด
    error_message = "ValueError: not enough values to unpack (expected 1, got 0)"
    
    # แก้ไขโค้ด
    fixed_code = code_agent.fix_bug(buggy_code, error_message)
    
    print("โค้ดที่มีบั๊ก:")
    print(buggy_code)
    print("\nโค้ดที่แก้ไขแล้ว:")
    print(fixed_code)


if __name__ == "__main__":
    main() 