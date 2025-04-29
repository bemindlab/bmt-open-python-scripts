# BMT Open Python Scripts

ชุดสคริปต์ Python สำหรับการทำงานอัตโนมัติและการพัฒนาแอปพลิเคชัน

## สารบัญ

- [การติดตั้ง](#การติดตั้ง)
- [การใช้งาน](#การใช้งาน)
- [การตั้งค่า Configuration](#การตั้งค่า-configuration)
- [การทำงานกับ AutoGen](#การทำงานกับ-autogen)
- [การทำงานกับ Webcam](#การทำงานกับ-webcam)
- [การทำงานกับ Git](#การทำงานกับ-git)
- [การแก้ไขปัญหา](#การแก้ไขปัญหา)

## การติดตั้ง

### 1. ติดตั้งผ่าน pip

```bash
# ติดตั้งแพ็คเกจหลัก
pip install bmt-scripts

# ติดตั้งแพ็คเกจเสริมทั้งหมด
pip install "bmt-scripts[all]"

# ติดตั้งแพ็คเกจเสริมเฉพาะส่วน
pip install "bmt-scripts[agents]"  # สำหรับ AutoGen
pip install "bmt-scripts[webcam]"  # สำหรับ Webcam
pip install "bmt-scripts[git]"     # สำหรับ Git
```

### 2. ติดตั้งจาก Source

```bash
# Clone repository
git clone https://github.com/bemindlab/bmt-open-python-scripts.git
cd bmt-open-python-scripts

# ติดตั้งในโหมด development
pip install -e ".[all]"
```

## การใช้งาน

### 1. การใช้งานผ่าน CLI

```bash
# แสดงความช่วยเหลือ
bmtlab --help

# แสดงหมวดหมู่คำสั่ง
bmtlab agents --help
bmtlab webcam --help
bmtlab git --help
```

### 2. การใช้งานผ่าน Python

```python
from bmt_libs.agents.autogen import CodeAgent
from bmt_libs.webcam import WebcamCapture
from bmt_libs.git import GitManager

# ใช้งาน AutoGen
code_agent = CodeAgent()
result = code_agent.write_code("เขียนฟังก์ชันคำนวณตัวเลข Fibonacci")

# ใช้งาน Webcam
webcam = WebcamCapture()
webcam.start()

# ใช้งาน Git
git = GitManager()
commits = git.get_recent_commits()
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
    "model": "gpt-3.5-turbo",  # โมเดลที่ใช้
    "temperature": 0.7,        # ค่าความสุ่มในการตอบ
    "max_tokens": 2000,        # จำนวน token สูงสุดต่อการตอบ
}
```

## การทำงานกับ AutoGen

AutoGen เป็นเครื่องมือที่ช่วยให้สามารถสร้างและใช้งาน AI agents ได้อย่างมีประสิทธิภาพ

### 1. ประเภทของ Agents

- **CodeAgent**: สำหรับการเขียนและแก้ไขโค้ด
- **ResearchAgent**: สำหรับการค้นคว้าและวิเคราะห์ข้อมูล
- **CreativeAgent**: สำหรับการสร้างเนื้อหาเชิงสร้างสรรค์

### 2. ตัวอย่างการใช้งาน

```python
from bmt_libs.agents.autogen import CodeAgent, ResearchAgent, CreativeAgent

# สร้าง agents
code_agent = CodeAgent()
research_agent = ResearchAgent()
creative_agent = CreativeAgent()

# เขียนโค้ด
code = code_agent.write_code("เขียนฟังก์ชันคำนวณตัวเลข Fibonacci")

# ค้นคว้าข้อมูล
research = research_agent.research("ประโยชน์ของ Python")

# เขียนบทความ
article = creative_agent.write_article("อนาคตของ AI")
```

## การทำงานกับ Webcam

### 1. การใช้งานพื้นฐาน

```python
from bmt_libs.webcam import WebcamCapture

# สร้าง instance
webcam = WebcamCapture()

# เริ่มการทำงาน
webcam.start()

# หยุดการทำงาน
webcam.stop()
```

### 2. การตั้งค่า

```python
from bmt_libs.webcam import WebcamConfig

# ตั้งค่ากล้อง
config = WebcamConfig(
    camera_id=0,
    width=640,
    height=480,
    fps=30
)

# สร้าง instance ด้วยการตั้งค่า
webcam = WebcamCapture(config)
```

## การทำงานกับ Git

### 1. การใช้งานพื้นฐาน

```python
from bmt_libs.git import GitManager

# สร้าง instance
git = GitManager()

# ดึงข้อมูล commit ล่าสุด
commits = git.get_recent_commits()

# สรุปการเปลี่ยนแปลง
summary = git.summarize_changes()
```

### 2. การตั้งค่า

```python
from bmt_libs.git import GitConfig

# ตั้งค่า Git
config = GitConfig(
    max_commits=10,
    exclude_patterns=["*.log", "*.tmp"]
)

# สร้าง instance ด้วยการตั้งค่า
git = GitManager(config)
```

## การแก้ไขปัญหา

### 1. ปัญหาการติดตั้ง

ถ้าคุณเจอข้อผิดพลาด:
```
Error: Package not found
```

ให้ตรวจสอบว่า:
- Python เวอร์ชัน 3.8 ขึ้นไป
- pip เป็นเวอร์ชันล่าสุด
- มีการเชื่อมต่ออินเทอร์เน็ต

### 2. ปัญหา AutoGen

ถ้าคุณเจอข้อผิดพลาด:
```
Error: AutoGen is not available
```

ให้รันคำสั่ง:
```bash
pip install "bmt-scripts[agents]"
pip install "ag2[openai]"
```

### 3. ปัญหา Webcam

ถ้าคุณเจอข้อผิดพลาด:
```
Error: Cannot open camera
```

ให้ตรวจสอบว่า:
- กล้องเว็บแคมเชื่อมต่อถูกต้อง
- มีสิทธิ์เข้าถึงกล้อง
- ไม่มีโปรแกรมอื่นใช้งานกล้องอยู่

### 4. ปัญหา Git

ถ้าคุณเจอข้อผิดพลาด:
```
Error: Not a git repository
```

ให้ตรวจสอบว่า:
- อยู่ในโฟลเดอร์ที่เป็น git repository
- git ถูกติดตั้งและตั้งค่าถูกต้อง

## การสนับสนุน

หากพบปัญหาหรือมีคำถาม สามารถ:
1. เปิด Issue ที่ [GitHub](https://github.com/bemindlab/bmt-open-python-scripts/issues)
2. ติดต่อทีมพัฒนาผ่าน [Email](mailto:support@bemindlab.com)
3. เข้าร่วม [Discord Community](https://discord.gg/bemindlab)
