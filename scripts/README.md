# Scripts Configuration

เอกสารนี้อธิบายการตั้งค่า configuration สำหรับ scripts ต่างๆ ในโปรเจค

## โครงสร้างไฟล์

```
scripts/
├── config.py          # ไฟล์ configuration หลัก
├── agents/           # สคริปต์สำหรับ AutoGen agents
├── webcam/          # สคริปต์สำหรับการทำงานกับกล้องเว็บแคม
└── git/             # สคริปต์สำหรับการทำงานกับ Git
```

## การตั้งค่า Configuration

### 1. Environment Variables

ต้องตั้งค่า environment variables ต่อไปนี้:

```bash
# OpenAI API Key สำหรับ AutoGen
export OPENAI_API_KEY=your-api-key
```

หรือสร้างไฟล์ `.env` ในโฟลเดอร์หลักของโปรเจค:

```
OPENAI_API_KEY=your-api-key
```

### 2. Webcam Configuration

การตั้งค่าสำหรับกล้องเว็บแคม:

```python
WEBCAM_CONFIG = {
    "default_camera": 0,  # ใช้กล้องแรกเป็นค่าเริ่มต้น
    "frame_width": 640,   # ความกว้างของภาพ
    "frame_height": 480,  # ความสูงของภาพ
    "fps": 30,           # เฟรมต่อวินาที
}
```

### 3. Git Configuration

การตั้งค่าสำหรับสคริปต์ Git:

```python
GIT_CONFIG = {
    "max_commits": 10,  # จำนวน commit สูงสุดที่จะแสดงในสรุป
    "exclude_patterns": [  # รูปแบบไฟล์ที่จะไม่รวมในการสรุป
        "*.log",
        "*.tmp",
        "__pycache__",
    ],
}
```

### 4. AutoGen Configuration

การตั้งค่าสำหรับ AutoGen agents:

```python
AUTOGEN_CONFIG = {
    "model": "gpt-4",      # โมเดลที่ใช้
    "temperature": 0.7,    # ค่าความสุ่มในการตอบ
    "max_tokens": 2000,    # จำนวน token สูงสุดต่อการตอบ
}
```

## การใช้งาน Configuration

### 1. นำเข้า Configuration

```python
from scripts.config import get_config, validate_config

# ดึงการตั้งค่าทั้งหมด
config = get_config()

# ตรวจสอบการตั้งค่า
if validate_config():
    print("Configuration is valid")
```

### 2. ใช้งานการตั้งค่าเฉพาะส่วน

```python
from scripts.config import WEBCAM_CONFIG, GIT_CONFIG, AUTOGEN_CONFIG

# ใช้งานการตั้งค่ากล้องเว็บแคม
camera_id = WEBCAM_CONFIG["default_camera"]
frame_width = WEBCAM_CONFIG["frame_width"]

# ใช้งานการตั้งค่า Git
max_commits = GIT_CONFIG["max_commits"]

# ใช้งานการตั้งค่า AutoGen
model = AUTOGEN_CONFIG["model"]
```

## การตรวจสอบ Configuration

รันไฟล์ `config.py` เพื่อตรวจสอบการตั้งค่าทั้งหมด:

```bash
python scripts/config.py
```

## หมายเหตุ

- การตั้งค่าทั้งหมดสามารถแก้ไขได้ในไฟล์ `config.py`
- ควรตรวจสอบการตั้งค่าก่อนใช้งานสคริปต์ต่างๆ
- หากต้องการเพิ่มการตั้งค่าใหม่ ให้เพิ่มในไฟล์ `config.py` และอัปเดตเอกสารนี้ 