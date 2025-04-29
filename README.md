# BMT Open Python Scripts

BMT Open Python Scripts เป็นชุดของสคริปต์และยูทิลิตี้ Python ที่จัดระเบียบเป็นแพ็คเกจ Python มาตรฐาน ให้เครื่องมือสำหรับนักพัฒนาในหลายสาขา

## 📚 ภาพรวม

โปรเจคนี้มีเครื่องมือในหมวดหมู่ต่อไปนี้:

- **ฮาร์ดแวร์**: เครื่องมือหลักสำหรับการโต้ตอบกับฮาร์ดแวร์
  - **เว็บแคม**: การจัดการอุปกรณ์กล้อง
    - แสดงรายการอุปกรณ์กล้องที่มี
    - แสดงภาพจากกล้องแบบเรียลไทม์
    - จับภาพและวิดีโอ
  - **หน้าจอ**: ยูทิลิตี้การจับภาพหน้าจอ
    - ถ่ายภาพหน้าจอ
    - บันทึกกิจกรรมบนหน้าจอ
- **Git**: ยูทิลิตี้สำหรับทำงานกับ Git repositories
  - สร้างสรุปการ commit
  - วิเคราะห์ประวัติ repository
- **Agents**: เครื่องมือสำหรับทำงานกับ AI agents
  - **AutoGen**: การรวมกับเฟรมเวิร์ค AutoGen ของ Microsoft
    - การสร้างและแก้ไขโค้ด
    - การช่วยเหลือในการวิจัย
    - การสร้างเนื้อหาสร้างสรรค์
  - เครื่องมือสร้าง mockup อย่างง่าย

## 🛠️ การติดตั้ง

### วิธีที่ 1: ติดตั้งผ่าน pip
```bash
pip install bmt-scripts
```

พร้อมกับแพ็คเกจเสริม:
```bash
# ติดตั้งพร้อมกับแพ็คเกจเสริมสำหรับ AI agent
pip install "bmt-scripts[agents]"

# ติดตั้งพร้อมกับแพ็คเกจเสริมสำหรับฮาร์ดแวร์
pip install "bmt-scripts[hardware]"

# ติดตั้งพร้อมกับแพ็คเกจเสริมสำหรับการพัฒนา
pip install "bmt-scripts[dev]"

# ติดตั้งพร้อมกับแพ็คเกจเสริมทั้งหมด
pip install "bmt-scripts[all]"
```

### วิธีที่ 2: ติดตั้งจากซอร์ส
1. คลอน repository:
```bash
git clone https://github.com/bemindlab/bmt-open-python-scripts.git
cd bmt-open-python-scripts
```

2. สร้างสภาพแวดล้อมเสมือน:
```bash
python -m venv .venv
source venv/bin/activate  # สำหรับ Linux/Mac
# หรือ
.\venv\Scripts\activate  # สำหรับ Windows
```

3. ติดตั้งในโหมดการพัฒนา:
```bash
pip install -e .
```

## 🚀 การใช้งาน

### วิธีที่ 1: ใช้คำสั่ง bmtlab

หลังจากติดตั้งแพ็คเกจแล้ว คุณสามารถรันโปรแกรมด้วยคำสั่งต่อไปนี้:

```bash
# แสดงหมวดหมู่และคำสั่งทั้งหมด
bmtlab --help

# เครื่องมือฮาร์ดแวร์
bmtlab hardware --help

# แสดงภาพจากกล้อง
bmtlab hardware webcam show --camera-id 0

# แสดงรายการกล้องที่มี
bmtlab hardware webcam list

# ถ่ายภาพหน้าจอ
bmtlab hardware screen capture

# เครื่องมือ Git
bmtlab git commit-summary

# เครื่องมือ AI agent
bmtlab agents --help

# สร้าง mockup ด้วย AI
bmtlab agents mockup --prompt "สร้าง mockup โปรไฟล์ผู้ใช้"

# ใช้ AutoGen agents (ต้องติดตั้งแพ็คเกจเสริม agents)
bmtlab agents autogen code --prompt "เขียนฟังก์ชันคำนวณตัวเลข Fibonacci"
bmtlab agents autogen research --topic "แนวทางปฏิบัติที่ดีของ Python"
bmtlab agents autogen creative --topic "การสำรวจอวกาศ" --type article

# แสดงเวอร์ชันของแพ็คเกจ
bmtlab version
```

### วิธีที่ 2: การรันสคริปต์แบบเดิม
เพื่อความเข้ากันได้กับเวอร์ชันเก่า คุณสามารถรันสคริปต์โดยตรงได้:

```bash
# แสดงสคริปต์ที่มีทั้งหมด
bmtlab list

# รันสคริปต์ตามหมวดหมู่และชื่อ
bmtlab run -s webcam.show
bmtlab run -s git.commit-summary
bmtlab run -s agents.mockup
```

### วิธีที่ 3: ใช้เป็นไลบรารี Python

```python
# นำเข้าและใช้โมดูลไลบรารี (สำหรับคอมโพเนนต์ที่นำกลับมาใช้ใหม่)
from bmt_libs.hardware.camera import Camera
from bmt_libs.hardware.screen import Screen
from bmt_libs.agents.autogen.core import CodeAgent

# แสดงรายการกล้องที่มีทั้งหมด
camera = Camera()
cameras = camera.list_devices()
for idx, name in cameras.items():
    print(f"พบกล้อง: {name} (ID: {idx})")

# จับภาพจากกล้อง
camera = Camera(camera_id=0)
frame = camera.capture_frame()
camera.save_image(frame, "screenshot.jpg")
        
# ใช้การจับภาพหน้าจอ
screen = Screen()
screenshot = screen.capture()
screen.save_image(screenshot, "screenshot.png")

# นำเข้าและใช้โมดูลสคริปต์ (สำหรับการทำงานระดับสูง)
from bmt_scripts.webcam import list_cameras, capture_image
from bmt_scripts.hardware import screen_capture

# แสดงรายการกล้องโดยใช้โมดูลสคริปต์
cameras = list_cameras()
print(f"พบกล้อง {len(cameras)} ตัว")

# ถ่ายภาพหน้าจอ
image_path = screen_capture()
print(f"บันทึกภาพหน้าจอไปที่: {image_path}")

# ใช้ AI agents (พร้อมกับแพ็คเกจเสริม)
try:
    # สร้าง agent ที่มีความสามารถในการสร้างโค้ด
    agent = CodeAgent()
    code = agent.write_code("เขียนฟังก์ชันคำนวณแฟกทอเรียล")
    print(code)
except ImportError:
    print("AutoGen ไม่พร้อมใช้งาน ติดตั้งด้วย: pip install 'bmt-scripts[agents]'")
```

## 📁 โครงสร้างโปรเจค

โปรเจคนี้เป็นไปตามโครงสร้างแพ็คเกจ Python มาตรฐานโดยแยกความรับผิดชอบ:

```
bmt-scripts/
├── src/                        # โค้ดหลักของแพ็คเกจ
│   ├── __init__.py             # ไฟล์มาร์คเกอร์แพ็คเกจหลัก
│   ├── bmt_libs/               # โมดูลไลบรารี (ใช้งานภายใน)
│   │   ├── __init__.py
│   │   ├── agents/             # การใช้งาน Agents
│   │   │   └── autogen/        # ไลบรารี Microsoft AutoGen
│   │   └── hardware/           # ไลบรารีสำหรับเข้าถึงฮาร์ดแวร์
│   │       ├── camera.py       # ยูทิลิตี้กล้อง
│   │       └── screen.py       # ยูทิลิตี้หน้าจอ
│   └── bmt_scripts/            # โมดูลสคริปต์ที่สามารถรันได้
│       ├── __init__.py         # การเริ่มต้นแพ็คเกจ
│       ├── _version.py         # ข้อมูลเวอร์ชันที่สร้างขึ้น
│       ├── cli.py              # หน้าต่างการทำงานผ่านคำสั่ง
│       ├── config/             # การจัดการการตั้งค่า
│       │   └── settings.py
│       ├── webcam/             # ฟังก์ชันการทำงานของเว็บแคม
│       ├── git/                # ยูทิลิตี้ Git
│       ├── plugins/            # ระบบ Plugin
│       └── agents/             # สคริปต์ AI agent
├── tests/                      # ไฟล์ทดสอบ
├── docs/                       # เอกสาร
└── pyproject.toml              # การตั้งค่าโปรเจค
```

สำหรับรายละเอียดเพิ่มเติมเกี่ยวกับโครงสร้างโปรเจค ดูที่ [docs/project-structure.md](docs/project-structure.md)

## 🎯 คุณสมบัติ

- หน้าต่างการทำงานผ่านคำสั่งสำหรับเครื่องมือทั้งหมด
- เครื่องมือเว็บแคมสำหรับจับภาพและแสดงภาพจากกล้อง
- ยูทิลิตี้ Git สำหรับวิเคราะห์ repository
- เครื่องมือ AI agent พร้อมการรวมกับ AutoGen
- สถาปัตยกรรมแบบโมดูลาร์สำหรับการขยายที่ง่าย
- เอกสารและทดสอบที่ครอบคลุม

## 📝 การทดสอบ

รันการทดสอบด้วย:
```bash
python -m pytest
```

## 🤝 การมีส่วนร่วม

เรายินดีรับการมีส่วนร่วม! กรุณาอ่าน [CONTRIBUTING.md](CONTRIBUTING.md) สำหรับรายละเอียดเพิ่มเติม

## 📋 ข้อมูลเพิ่มเติม

- รองรับ Python 3.12+
- ใช้ pytest สำหรับการทดสอบ
- เข้ากันได้กับ Windows, Linux และ macOS
- ใช้ black และ isort สำหรับการจัดรูปแบบโค้ด
- ใช้ mypy สำหรับการตรวจสอบประเภท
- จัดการการพึ่งพาด้วย pyproject.toml

## 📄 ลิขสิทธิ์

โปรเจคนี้ได้รับลิขสิทธิ์ภายใต้ MIT License - ดูรายละเอียดที่ [LICENSE](LICENSE)

## 🔄 อัปเดตล่าสุด

- จัดระเบียบใหม่เป็นโครงสร้างแพ็คเกจคู่ (`bmt_libs` และ `bmt_scripts`)
- ปรับปรุงโครงสร้างโปรเจคตามแนวทางปฏิบัติที่ดีในการแพ็คเกจ Python
- เพิ่มการแยกความรับผิดชอบระหว่างไลบรารีและสคริปต์
- ขยายระบบ Plugin สำหรับการขยายความสามารถ
- เพิ่มการจัดระเบียบแพ็คเกจ Python ที่เหมาะสมพร้อมแพ็คเกจย่อยที่ชัดเจน
- ปรับปรุงอินเตอร์เฟซ CLI ด้วยคำสั่งเฉพาะโดเมน
- เพิ่มการจัดการการพึ่งพาเสริม
- ปรับปรุงเอกสารและตัวอย่าง