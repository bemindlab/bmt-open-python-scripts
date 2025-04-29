# AutoGen Core Feature Library

โมดูลนี้เป็น core feature library สำหรับ agent script โดยใช้ AutoGen จาก Microsoft ซึ่งเป็นเครื่องมือที่ช่วยให้สามารถสร้างและใช้งาน AI agents ได้อย่างมีประสิทธิภาพ

## สารบัญ

- [การติดตั้ง](#การติดตั้ง)
- [การใช้งานพื้นฐาน](#การใช้งานพื้นฐาน)
- [ประเภทของ Agents](#ประเภทของ-agents)
- [การทำงานร่วมกันระหว่าง Agents](#การทำงานร่วมกันระหว่าง-agents)
- [การทำงานกับไฟล์และข้อมูล](#การทำงานกับไฟล์และข้อมูล)
- [การตั้งค่า Configuration](#การตั้งค่า-configuration)
- [ตัวอย่างการใช้งาน](#ตัวอย่างการใช้งาน)
- [ข้อจำกัดและข้อควรระวัง](#ข้อจำกัดและข้อควรระวัง)

## การติดตั้ง

### 1. ติดตั้ง AutoGen ผ่าน pip

```bash
# ติดตั้งแพ็คเกจเสริมสำหรับ AI agent
pip install "bmt-scripts[agents]"

# ติดตั้ง OpenAI
pip install "ag2[openai]"
```

### 2. ตั้งค่า API key สำหรับ OpenAI

คุณจะต้องมี API key จาก OpenAI ก่อน ถ้ายังไม่มี ให้ทำตามขั้นตอนต่อไปนี้:

1. ไปที่ [OpenAI Platform](https://platform.openai.com/)
2. เข้าสู่ระบบหรือสร้างบัญชีใหม่
3. ไปที่ [Billing settings](https://platform.openai.com/account/billing/overview)
4. เพิ่มวิธีการชำระเงิน (Add payment method)
5. เพิ่มเงินเข้าไปในบัญชี (Add credits)
6. ไปที่ [API keys](https://platform.openai.com/api-keys)
7. คลิก "Create new secret key"
8. ตั้งชื่อให้กับ key (เช่น "BMT Scripts")
9. คัดลอก API key ที่ได้

จากนั้นตั้งค่า API key ด้วยวิธีใดวิธีหนึ่งต่อไปนี้:

#### วิธีที่ 1: ตั้งค่าผ่านตัวแปรสภาพแวดล้อม

```bash
export OPENAI_API_KEY=your-api-key
```

#### วิธีที่ 2: สร้างไฟล์ .env

สร้างไฟล์ `.env` ในโฟลเดอร์หลักของโปรเจค:

```
OPENAI_API_KEY=your-api-key
```

### การแก้ไขปัญหา

#### 1. ปัญหา API key ไม่ถูกต้อง

ถ้าคุณเจอข้อผิดพลาด:
```
Error code: 401 - Invalid Authentication
```

แสดงว่า API key ไม่ถูกต้อง ให้ตรวจสอบว่า:
- API key ถูกต้องและยังไม่หมดอายุ
- ตั้งค่า API key ถูกต้องในไฟล์ `.env` หรือตัวแปรสภาพแวดล้อม

#### 2. ปัญหาโควต้าไม่เพียงพอ

ถ้าคุณเจอข้อผิดพลาด:
```
Error code: 429 - You exceeded your current quota
```

แสดงว่าโควต้าการใช้งานไม่เพียงพอ ให้:
1. ตรวจสอบยอดเงินคงเหลือที่ [Billing usage](https://platform.openai.com/account/usage)
2. เพิ่มเงินในบัญชีที่ [Billing settings](https://platform.openai.com/account/billing/overview)

## การใช้งานพื้นฐาน

### การใช้งานผ่าน CLI

```bash
# แสดงหมวดหมู่และคำสั่งทั้งหมด
bmtlab --help

# แสดงคำสั่งของ AI agent
bmtlab agents --help

# ใช้ AutoGen agents
bmtlab agents autogen code --prompt "เขียนฟังก์ชันคำนวณตัวเลข Fibonacci"
bmtlab agents autogen research --topic "แนวทางปฏิบัติที่ดีของ Python"
bmtlab agents autogen creative --topic "การสำรวจอวกาศ" --type article
```

### การใช้งานผ่าน Python

#### AutoGenAgent

คลาสหลักสำหรับการใช้งาน AutoGen ซึ่งเป็นพื้นฐานสำหรับ agents อื่นๆ ทั้งหมด

```python
from bmt_libs.agents.autogen import AutoGenAgent

# สร้าง agent
agent = AutoGenAgent(
    name="my_agent",
    system_message="คุณเป็นผู้ช่วยที่ช่วยตอบคำถาม",
    api_key="your-api-key"  # ถ้าไม่ระบุจะใช้จากตัวแปรสภาพแวดล้อม OPENAI_API_KEY
)

# ส่งข้อความไปยัง agent
response = agent.chat("สวัสดี")

# รันโค้ดผ่าน agent
result = agent.execute_code("print('Hello, World!')")

# สร้าง group chat
group_chat = agent.create_group_chat(
    agents=[other_agent.agent],
    group_name="my_group_chat"
)

# รัน group chat
result = agent.run_group_chat(group_chat, "หัวข้อสำหรับ group chat")
```

## ประเภทของ Agents

### CodeAgent

Agent สำหรับการเขียนและแก้ไขโค้ด

```python
from bmt_libs.agents.autogen import CodeAgent

# สร้าง code agent
code_agent = CodeAgent(api_key="your-api-key")

# เขียนโค้ดตามคำอธิบาย
code = code_agent.write_code("เขียนฟังก์ชัน Python สำหรับคำนวณค่าเฉลี่ยของรายการตัวเลข")

# แก้ไขบั๊กในโค้ด
fixed_code = code_agent.fix_bug(
    code="def add(a, b): return a - b",  # โค้ดที่มีบั๊ก
    error_message="ฟังก์ชัน add ควรบวกเลข ลบเลข"  # ข้อความแสดงข้อผิดพลาด
)

# ปรับปรุงโค้ดให้มีประสิทธิภาพและอ่านง่ายขึ้น
refactored_code = code_agent.refactor_code(
    code="""
    def process_data(data):
        result = []
        for item in data:
            if item > 0:
                result.append(item * 2)
        return result
    """
)
```

### ResearchAgent

Agent สำหรับการค้นคว้าและวิเคราะห์ข้อมูล

```python
from bmt_libs.agents.autogen import ResearchAgent

# สร้าง research agent
research_agent = ResearchAgent(api_key="your-api-key")

# ค้นคว้าข้อมูลเกี่ยวกับหัวข้อที่กำหนด
research_result = research_agent.research("ประโยชน์ของ Python ในการพัฒนาเว็บแอปพลิเคชัน")

# วิเคราะห์ข้อมูล
analysis_result = research_agent.analyze_data("ข้อมูลที่ต้องการวิเคราะห์")
```

### CreativeAgent

Agent สำหรับการสร้างเนื้อหาเชิงสร้างสรรค์

```python
from bmt_libs.agents.autogen import CreativeAgent

# สร้าง creative agent
creative_agent = CreativeAgent(api_key="your-api-key")

# เขียนบทความ
article = creative_agent.write_article(
    topic="อนาคตของปัญญาประดิษฐ์ในประเทศไทย",
    length="medium"  # short, medium, long
)

# สร้างไอเดีย
ideas = creative_agent.generate_ideas("แอปพลิเคชันสำหรับการจัดการงาน")
```

## การทำงานร่วมกันระหว่าง Agents

### Group Chat

```python
from bmt_libs.agents.autogen import CodeAgent, ResearchAgent, CreativeAgent

# สร้าง agents
code_agent = CodeAgent(api_key="your-api-key")
research_agent = ResearchAgent(api_key="your-api-key")
creative_agent = CreativeAgent(api_key="your-api-key")

# สร้าง group chat
group_chat = code_agent.create_group_chat(
    agents=[research_agent.agent, creative_agent.agent],
    group_name="project_planning"
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
result = code_agent.run_group_chat(group_chat, topic)
print(f"ผลลัพธ์ของ group chat:\n{result['summary']}")
```

## การทำงานกับไฟล์และข้อมูล

### การทำงานกับไฟล์ JSON

```python
import json
from bmt_libs.agents.autogen import CodeAgent

# สร้าง code agent
code_agent = CodeAgent(api_key=api_key)

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

# อ่านข้อมูลจากไฟล์ JSON
with open("data.json", "r", encoding="utf-8") as f:
    loaded_data = json.load(f)
```

### การทำงานกับไฟล์ CSV

```python
import csv
from bmt_libs.agents.autogen import CodeAgent

# สร้าง code agent
code_agent = CodeAgent(api_key=api_key)

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

# อ่านข้อมูลจากไฟล์ CSV
with open("data.csv", "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    loaded_csv_data = list(reader)
```

### การแปลงข้อมูลระหว่างรูปแบบ

```python
import json
import csv
from bmt_libs.agents.autogen import CodeAgent, ResearchAgent

# สร้าง agents
code_agent = CodeAgent(api_key=api_key)
research_agent = ResearchAgent(api_key=api_key)

# อ่านข้อมูลจากไฟล์ CSV
with open("data.csv", "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    headers = next(reader)  # อ่านส่วนหัว
    csv_data = list(reader)

# แปลงข้อมูล CSV เป็น JSON
json_data = []
for row in csv_data:
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
    
    json_data.append(item)

# บันทึกข้อมูลที่แปลงแล้วลงในไฟล์ JSON
with open("csv_to_json.json", "w", encoding="utf-8") as f:
    json.dump({"users": json_data}, f, ensure_ascii=False, indent=4)

# วิเคราะห์ข้อมูลโดยใช้ ResearchAgent
data_to_analyze = json.dumps(json_data, ensure_ascii=False, indent=2)
analysis_result = research_agent.analyze_data(data_to_analyze)
```

## การตั้งค่า Configuration

### การตั้งค่า AutoGen

AutoGen สามารถตั้งค่าได้ผ่านไฟล์ `scripts/config.py`:

```python
# AutoGen configuration
AUTOGEN_CONFIG = {
    "model": "gpt-4",  # โมเดลที่ใช้สำหรับ AutoGen
    "temperature": 0.7,  # ค่าความสุ่มในการตอบ
    "max_tokens": 2000,  # จำนวน token สูงสุดต่อการตอบ
}
```

### การใช้งาน Configuration

```python
from bmt_scripts.configimport AUTOGEN_CONFIG, validate_config

# ตรวจสอบการตั้งค่า
if validate_config():
    # ใช้งานการตั้งค่า
    model = AUTOGEN_CONFIG["model"]
    temperature = AUTOGEN_CONFIG["temperature"]
    
    # สร้าง agent ด้วยการตั้งค่าที่กำหนด
    agent = AutoGenAgent(
        name="my_agent",
        system_message="คุณเป็นผู้ช่วยที่ช่วยตอบคำถาม",
        model=model,
        temperature=temperature
    )
else:
    print("กรุณาตั้งค่า configuration ให้ถูกต้อง")
```

### การตั้งค่า Environment Variables

ต้องตั้งค่า environment variables ต่อไปนี้:

```bash
# OpenAI API Key สำหรับ AutoGen
export OPENAI_API_KEY=your-api-key
```

หรือสร้างไฟล์ `.env` ในโฟลเดอร์หลักของโปรเจค:

```
OPENAI_API_KEY=your-api-key
```

## ตัวอย่างการใช้งาน

### ตัวอย่างการใช้งาน AutoGen

```python
#!/usr/bin/env python3
"""
ตัวอย่างการใช้งาน AutoGen
"""

import os
from bmt_libs.agents.autogen import CodeAgent, ResearchAgent, CreativeAgent

# ตรวจสอบ API key
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("กรุณาตั้งค่า OPENAI_API_KEY ในตัวแปรสภาพแวดล้อม")
    exit(1)

# สร้าง agents
code_agent = CodeAgent(api_key=api_key)
research_agent = ResearchAgent(api_key=api_key)
creative_agent = CreativeAgent(api_key=api_key)

# ตัวอย่างการใช้งาน CodeAgent
code_description = "เขียนฟังก์ชัน Python สำหรับคำนวณค่าเฉลี่ยของรายการตัวเลข"
code_result = code_agent.write_code(code_description)
print(f"คำอธิบาย: {code_description}")
print(f"โค้ดที่ได้:\n{code_result}")

# ตัวอย่างการใช้งาน ResearchAgent
research_topic = "ประโยชน์ของ Python ในการพัฒนาเว็บแอปพลิเคชัน"
research_result = research_agent.research(research_topic)
print(f"หัวข้อ: {research_topic}")
print(f"ผลการค้นคว้า:\n{research_result}")

# ตัวอย่างการใช้งาน CreativeAgent
article_topic = "อนาคตของปัญญาประดิษฐ์ในประเทศไทย"
article_result = creative_agent.write_article(article_topic, length="short")
print(f"หัวข้อ: {article_topic}")
print(f"บทความ:\n{article_result}")
```

### ตัวอย่างการใช้งาน AutoGen Group Chat

```python
#!/usr/bin/env python3
"""
ตัวอย่างการใช้งาน AutoGen Group Chat
"""

import os
from bmt_libs.agents.autogen import CodeAgent, ResearchAgent, CreativeAgent

# ตรวจสอบ API key
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("กรุณาตั้งค่า OPENAI_API_KEY ในตัวแปรสภาพแวดล้อม")
    exit(1)

# สร้าง agents
code_agent = CodeAgent(api_key=api_key)
research_agent = ResearchAgent(api_key=api_key)
creative_agent = CreativeAgent(api_key=api_key)

# สร้าง group chat
group_chat = code_agent.create_group_chat(
    agents=[research_agent.agent, creative_agent.agent],
    group_name="project_planning"
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
result = code_agent.run_group_chat(group_chat, topic)
print(f"ผลลัพธ์ของ group chat:\n{result['summary']}")
```

### ตัวอย่างการใช้งาน AutoGen ในการทำงานกับไฟล์และข้อมูล

```python
#!/usr/bin/env python3
"""
ตัวอย่างการใช้งาน AutoGen ในการทำงานกับไฟล์และข้อมูล
"""

import os
import json
import csv
from bmt_libs.agents.autogen import CodeAgent, ResearchAgent

# ตรวจสอบ API key
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("กรุณาตั้งค่า OPENAI_API_KEY ในตัวแปรสภาพแวดล้อม")
    exit(1)

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

# อ่านข้อมูลจากไฟล์ JSON
with open("data.json", "r", encoding="utf-8") as f:
    loaded_data = json.load(f)

print("ข้อมูล JSON ที่สร้าง:")
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

# อ่านข้อมูลจากไฟล์ CSV
with open("data.csv", "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    loaded_csv_data = list(reader)

print("ข้อมูล CSV ที่สร้าง:")
for row in loaded_csv_data:
    print(row)

# ตัวอย่างการแปลงข้อมูล CSV เป็น JSON
print("\n=== ตัวอย่างการแปลงข้อมูล CSV เป็น JSON ===")

# อ่านข้อมูลจากไฟล์ CSV
with open("data.csv", "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    headers = next(reader)  # อ่านส่วนหัว
    csv_data = list(reader)

# แปลงข้อมูล CSV เป็น JSON
json_data = []
for row in csv_data:
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
    
    json_data.append(item)

# บันทึกข้อมูลที่แปลงแล้วลงในไฟล์ JSON
with open("csv_to_json.json", "w", encoding="utf-8") as f:
    json.dump({"users": json_data}, f, ensure_ascii=False, indent=4)

print("ข้อมูลที่แปลงจาก CSV เป็น JSON:")
print(json.dumps(json_data, ensure_ascii=False, indent=2))

# ตัวอย่างการวิเคราะห์ข้อมูล
print("\n=== ตัวอย่างการวิเคราะห์ข้อมูล ===")

# วิเคราะห์ข้อมูลโดยใช้ ResearchAgent
data_to_analyze = json.dumps(json_data, ensure_ascii=False, indent=2)
analysis_result = research_agent.analyze_data(data_to_analyze)
```

## ข้อจำกัดและข้อควรระวัง

1. **ค่าใช้จ่าย**: การใช้งาน AutoGen ต้องใช้ API ของ OpenAI ซึ่งมีค่าใช้จ่าย
2. **ข้อจำกัดของ API**: OpenAI API มีข้อจำกัดในการใช้งาน เช่น จำนวน token สูงสุดต่อการเรียก
3. **ความปลอดภัย**: ควรระวังการส่งข้อมูลที่สำคัญหรือข้อมูลส่วนตัวไปยัง API
4. **ประสิทธิภาพ**: การใช้งาน AutoGen อาจใช้เวลานานขึ้นอยู่กับความซับซ้อนของงาน
5. **การตั้งค่า**: ควรตรวจสอบการตั้งค่าใน `bmt-scripts/config/settings.py` ก่อนใช้งาน

## การแก้ไขปัญหาที่พบบ่อย

### 1. ImportError: AutoGen is not available

ถ้าคุณเจอข้อผิดพลาด:
```
Error: AutoGen is not available. Install with: pip install 'bmt-scripts[agents]'
```

แสดงว่ายังไม่ได้ติดตั้งแพ็คเกจเสริมสำหรับ AI agent ให้รันคำสั่ง:
```bash
pip install "bmt-scripts[agents]"
```

### 2. ImportError: 'openai' is not installed

ถ้าคุณเจอข้อผิดพลาด:
```
ImportError: A module needed for autogen.oai.client.create_openai_client is missing:
 - 'openai' is not installed.
```

แสดงว่ายังไม่ได้ติดตั้งแพ็คเกจ OpenAI ให้รันคำสั่ง:
```bash
pip install "ag2[openai]"
```

### 3. Error: Invalid Authentication

ถ้าคุณเจอข้อผิดพลาด:
```
Error code: 401 - Invalid Authentication
```

แสดงว่า API key ไม่ถูกต้อง ให้ตรวจสอบว่า:
- API key ถูกต้องและยังไม่หมดอายุ
- ตั้งค่า API key ถูกต้องในไฟล์ `.env` หรือตัวแปรสภาพแวดล้อม

### 4. Error: Insufficient Quota

ถ้าคุณเจอข้อผิดพลาด:
```
Error code: 429 - You exceeded your current quota
```

แสดงว่าโควต้าการใช้งานไม่เพียงพอ ให้:
1. ตรวจสอบยอดเงินคงเหลือที่ [Billing usage](https://platform.openai.com/account/usage)
2. เพิ่มเงินในบัญชีที่ [Billing settings](https://platform.openai.com/account/billing/overview)

### 5. Error: Model not found

ถ้าคุณเจอข้อผิดพลาด:
```
Error code: 404 - The model `gpt-4` does not exist or you do not have access to it
```

แสดงว่าคุณไม่มีสิทธิ์เข้าถึงโมเดลที่ระบุ ให้:
1. ตรวจสอบว่าคุณมีสิทธิ์เข้าถึงโมเดลที่ต้องการใช้
2. ลองเปลี่ยนไปใช้โมเดลอื่นที่คุณมีสิทธิ์เข้าถึง เช่น `gpt-3.5-turbo`

### 6. ปัญหาอื่นๆ

ถ้าคุณเจอปัญหาอื่นๆ ให้:
1. ตรวจสอบว่าติดตั้งแพ็คเกจทั้งหมดครบถ้วน:
   ```bash
   pip install "bmt-scripts[all]"
   ```
2. อัปเดตแพ็คเกจให้เป็นเวอร์ชันล่าสุด:
   ```bash
   pip install --upgrade "bmt-scripts[all]"
   ```
3. ตรวจสอบ log เพื่อดูรายละเอียดข้อผิดพลาด
4. รายงานปัญหาที่พบที่ [GitHub Issues](https://github.com/bemindlab/bmt-open-python-scripts/issues)
