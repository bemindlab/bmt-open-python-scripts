# BMT Open Python Scripts

## 📚 เกี่ยวกับ
BMT Open Python Scripts เป็นชุดสคริปต์ Python ที่รวบรวมเครื่องมือและสคริปต์ที่มีประโยชน์สำหรับนักพัฒนา โดยมีสคริปต์ในหมวดหมู่ต่างๆ ดังนี้:

- **Webcam**: สคริปต์สำหรับจัดการกล้องเว็บแคม
  - `list.py`: แสดงรายการกล้องเว็บแคมที่มีในระบบ
  - `show.py`: แสดงภาพจากกล้องเว็บแคมแบบเรียลไทม์
- **Git**: สคริปต์สำหรับการทำงานกับ Git
  - `commit-summary.py`: สร้างสรุปการ commit โดยใช้ AI
- **Agents**: สคริปต์สำหรับการใช้งาน AI Agents
  - `autogen_example.py`: ตัวอย่างการใช้งาน AutoGen
  - `autogen_group_chat.py`: ตัวอย่างการใช้งาน AutoGen Group Chat
  - `autogen_file_operations.py`: ตัวอย่างการใช้งาน AutoGen ในการทำงานกับไฟล์และข้อมูล

## 🛠️ การติดตั้ง

### วิธีที่ 1: ติดตั้งผ่าน pip
```bash
pip install bmt-open-python-scripts
```

### วิธีที่ 2: ติดตั้งจากซอร์สโค้ด
1. โคลนโปรเจค:
```bash
git clone https://github.com/bemindlab/bmt-open-python-scripts.git
cd bmt-open-python-scripts
```

2. สร้าง virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # สำหรับ Linux/Mac
# หรือ
.\venv\Scripts\activate  # สำหรับ Windows
```

3. ติดตั้ง dependencies:
```bash
pip install -r requirements.txt
```

## 🚀 การใช้งาน

### วิธีที่ 1: ใช้งานผ่านคำสั่ง bmtlab
หลังจากติดตั้งแพ็คเกจแล้ว สามารถรันโปรแกรมได้ด้วยคำสั่ง:
```bash
# แสดงรายการสคริปต์ทั้งหมด
bmtlab list

# รันสคริปต์ที่ต้องการ
bmtlab run -s หมวดหมู่.ชื่อสคริปต์

# ตัวอย่าง: รันสคริปต์แสดงภาพจากเว็บแคม
bmtlab run -s webcam.show

# ตัวอย่าง: รันสคริปต์ตัวอย่างการใช้งาน AutoGen
bmtlab run -s agents.autogen_example

# แสดงเวอร์ชันของแพ็คเกจ
bmtlab version
```

### วิธีที่ 2: รันไฟล์ main.py โดยตรง
```bash
# เข้าไปยังโฟลเดอร์ src/bmt_open_python_scripts
cd src/bmt_open_python_scripts

# รันโปรแกรมหลัก
python main.py [คำสั่ง] [ตัวเลือก]

# ตัวอย่าง:
python main.py list  # แสดงรายการสคริปต์
python main.py run -s webcam.show  # รันสคริปต์แสดงภาพจากเว็บแคม
python main.py run -s agents.autogen_example  # รันสคริปต์ตัวอย่างการใช้งาน AutoGen
python main.py version  # แสดงเวอร์ชันของแพ็คเกจ
```

## 📁 โครงสร้างโปรเจค
```
bmt-open-python-scripts/
├── src/
│   └── bmt_open_python_scripts/
│       ├── __init__.py
│       ├── _version.py
│       └── main.py
├── lib/
│   └── agents/
│       ├── __init__.py
│       ├── autogen.py
│       ├── camera.py
│       └── README.md
├── scripts/
│   ├── agents/
│   │   ├── autogen_example.py
│   │   ├── autogen_group_chat.py
│   │   ├── autogen_file_operations.py
│   │   └── mockup.py
│   ├── git/
│   └── webcam/
├── docs/
│   └── autogen.md
├── tests/
├── requirements.txt
├── setup.py
└── README.md
```

## 🎯 ฟีเจอร์
- แสดงรายการสคริปต์แยกตามหมวดหมู่
- ค้นหาสคริปต์ด้วยชื่อ คำอธิบาย หรือหมวดหมู่
- แสดงรายละเอียดของสคริปต์ก่อนรัน
- รองรับการรันสคริปต์ Python, Shell และ Batch
- แสดงผลด้วยสีสันสวยงาม
- **AutoGen Core Feature Library**: ชุดเครื่องมือสำหรับการสร้างและใช้งาน AI Agents
  - CodeAgent: สำหรับการเขียนและแก้ไขโค้ด
  - ResearchAgent: สำหรับการค้นคว้าและวิเคราะห์ข้อมูล
  - CreativeAgent: สำหรับการสร้างสรรค์เนื้อหา
  - Group Chat: สำหรับการทำงานร่วมกันระหว่าง Agents

## 📝 การทดสอบ
รันการทดสอบด้วยคำสั่ง:
```bash
python -m pytest tests/
```

## 🤝 การมีส่วนร่วม
เรายินดีรับการมีส่วนร่วมจากทุกท่าน! กรุณาอ่าน [CONTRIBUTING.md](CONTRIBUTING.md) สำหรับรายละเอียดเพิ่มเติม

## 📋 รายละเอียดเพิ่มเติม
- รองรับ Python 3.12 ขึ้นไป
- ใช้ pytest สำหรับการทดสอบ
- รองรับการทำงานบน Windows, Linux และ macOS
- ใช้ black และ flake8 สำหรับการจัดรูปแบบโค้ด
- ใช้ mypy สำหรับการตรวจสอบ type

## 📄 ลิขสิทธิ์
โปรเจคนี้อยู่ภายใต้ลิขสิทธิ์ MIT License - ดูรายละเอียดเพิ่มเติมได้ที่ [LICENSE](LICENSE)

## 🔄 การอัปเดตล่าสุด
- เพิ่มโครงสร้างโปรเจคในเอกสาร
- ปรับปรุงคำอธิบายการติดตั้งและการใช้งาน
- เพิ่มข้อมูลเกี่ยวกับการทดสอบและการมีส่วนร่วม
