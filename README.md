# BMT Open Python Scripts

## 📚 เกี่ยวกับ
BMT Open Python Scripts เป็นชุดสคริปต์ Python ที่รวบรวมเครื่องมือและสคริปต์ที่มีประโยชน์สำหรับนักพัฒนา โดยมีสคริปต์ในหมวดหมู่ต่างๆ ดังนี้:

- **Webcam**: สคริปต์สำหรับจัดการกล้องเว็บแคม
  - `list.py`: แสดงรายการกล้องเว็บแคมที่มีในระบบ
  - `show.py`: แสดงภาพจากกล้องเว็บแคมแบบเรียลไทม์
- **Git**: สคริปต์สำหรับการทำงานกับ Git
  - `commit-summary.py`: สร้างสรุปการ commit โดยใช้ AI

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
