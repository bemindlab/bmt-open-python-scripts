# โครงสร้างโปรเจค (Project Structure)

เอกสารนี้อธิบายโครงสร้างของโปรเจค BMT Open Python Scripts

## โครงสร้างหลัก

```
bmt-open-python-scripts/
├── .github/                    # การตั้งค่า GitHub
│   └── workflows/             # GitHub Actions workflows
│       ├── release.yml        # Workflow สำหรับการ release
│       └── test.yml           # Workflow สำหรับการทดสอบ
│
├── docs/                      # เอกสาร
│   ├── autogen.md            # เอกสาร AutoGen
│   ├── project-structure.md  # เอกสารโครงสร้างโปรเจค
│   ├── release.md            # เอกสารการ release
│   └── testing.md            # เอกสารการทดสอบ
│
├── lib/                       # โมดูลหลัก
│   ├── agents/               # โมดูล agents
│   │   ├── __init__.py
│   │   └── autogen.py        # โมดูล AutoGen
│   │
│   ├── utils/                # โมดูล utilities
│   │   ├── __init__.py
│   │   ├── file.py          # ฟังก์ชันสำหรับการจัดการไฟล์
│   │   └── logger.py        # ฟังก์ชันสำหรับการ logging
│   │
│   └── __init__.py
│
├── scripts/                   # สคริปต์หลัก
│   ├── config.py             # การตั้งค่า configuration
│   ├── git/                  # สคริปต์ Git
│   │   ├── __init__.py
│   │   └── commit_summary.py # สคริปต์สรุป commit
│   │
│   ├── webcam/               # สคริปต์กล้องเว็บแคม
│   │   ├── __init__.py
│   │   ├── list.py          # สคริปต์แสดงรายการกล้อง
│   │   └── show.py          # สคริปต์แสดงภาพจากกล้อง
│   │
│   └── __init__.py
│
├── tests/                    # โมดูลทดสอบ
│   ├── __init__.py
│   ├── test_config.py       # ทดสอบ configuration
│   ├── test_webcam_list.py  # ทดสอบการแสดงรายการกล้อง
│   └── test_webcam_show.py  # ทดสอบการแสดงภาพจากกล้อง
│
├── .env                      # ไฟล์ environment variables
├── .gitignore               # ไฟล์ที่ Git จะไม่ติดตาม
├── CHANGELOG.md             # ประวัติการเปลี่ยนแปลง
├── LICENSE                  # ใบอนุญาต
├── README.md                # เอกสารหลัก
├── pyproject.toml           # การตั้งค่า Poetry
└── requirements.txt         # Dependencies
```

## รายละเอียดแต่ละส่วน

### 1. `.github/`

โฟลเดอร์สำหรับการตั้งค่า GitHub:

- `workflows/`: ไฟล์ GitHub Actions workflows
  - `release.yml`: Workflow สำหรับการ release
  - `test.yml`: Workflow สำหรับการทดสอบ

### 2. `docs/`

โฟลเดอร์สำหรับเอกสาร:

- `autogen.md`: เอกสาร AutoGen
- `project-structure.md`: เอกสารโครงสร้างโปรเจค
- `release.md`: เอกสารการ release
- `testing.md`: เอกสารการทดสอบ

### 3. `lib/`

โฟลเดอร์สำหรับโมดูลหลัก:

- `agents/`: โมดูล agents
  - `autogen.py`: โมดูล AutoGen
- `utils/`: โมดูล utilities
  - `file.py`: ฟังก์ชันสำหรับการจัดการไฟล์
  - `logger.py`: ฟังก์ชันสำหรับการ logging

### 4. `scripts/`

โฟลเดอร์สำหรับสคริปต์หลัก:

- `config.py`: การตั้งค่า configuration
- `git/`: สคริปต์ Git
  - `commit_summary.py`: สคริปต์สรุป commit
- `webcam/`: สคริปต์กล้องเว็บแคม
  - `list.py`: สคริปต์แสดงรายการกล้อง
  - `show.py`: สคริปต์แสดงภาพจากกล้อง

### 5. `tests/`

โฟลเดอร์สำหรับโมดูลทดสอบ:

- `test_config.py`: ทดสอบ configuration
- `test_webcam_list.py`: ทดสอบการแสดงรายการกล้อง
- `test_webcam_show.py`: ทดสอบการแสดงภาพจากกล้อง

### 6. ไฟล์หลัก

- `.env`: ไฟล์ environment variables
- `.gitignore`: ไฟล์ที่ Git จะไม่ติดตาม
- `CHANGELOG.md`: ประวัติการเปลี่ยนแปลง
- `LICENSE`: ใบอนุญาต
- `README.md`: เอกสารหลัก
- `pyproject.toml`: การตั้งค่า Poetry
- `requirements.txt`: Dependencies

## การตั้งค่า Configuration

การตั้งค่า Configuration อยู่ในไฟล์ `scripts/config.py`:

```python
# Configuration สำหรับสคริปต์ต่างๆ
WEBCAM_CONFIG = {
    "default_camera": 0,
    "frame_width": 640,
    "frame_height": 480,
    "fps": 30,
}

GIT_CONFIG = {
    "max_commits": 10,
    "exclude_patterns": [
        "*.log",
        "*.tmp",
        "__pycache__",
    ],
}

AUTOGEN_CONFIG = {
    "model": "gpt-4",
    "temperature": 0.7,
    "max_tokens": 2000,
}
```

## การตั้งค่า Environment Variables

ต้องตั้งค่า environment variables ต่อไปนี้:

```bash
# OpenAI API Key สำหรับ AutoGen
export OPENAI_API_KEY=your-api-key
```

หรือสร้างไฟล์ `.env` ในโฟลเดอร์หลักของโปรเจค:

```
OPENAI_API_KEY=your-api-key
```

## การตั้งค่า GitHub Actions

### 1. Release Workflow

ไฟล์ `.github/workflows/release.yml`:

```yaml
name: Release

on:
  push:
    tags:
      - 'v*'

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install build twine
      
      - name: Validate configuration
        run: |
          python -c "from scripts.config import validate_config; assert validate_config()"
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
      
      - name: Run tests
        run: |
          pip install pytest
          python -m pytest
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
      
      - name: Build package
        run: python -m build
      
      - name: Upload to PyPI
        run: |
          python -m twine upload dist/*
        env:
          TWINE_USERNAME: __token__
          TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
```

### 2. Test Workflow

ไฟล์ `.github/workflows/test.yml`:

```yaml
name: Test

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install pytest pytest-mock opencv-python
      
      - name: Run tests
        run: |
          python -m pytest
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
```

## หมายเหตุ

- โครงสร้างโปรเจคถูกออกแบบให้เป็นระเบียบและง่ายต่อการบำรุงรักษา
- แต่ละโมดูลมีหน้าที่ชัดเจนและไม่ซ้ำซ้อนกัน
- การตั้งค่า Configuration อยู่ในไฟล์เดียวเพื่อความสะดวกในการจัดการ
- มีการทดสอบครอบคลุมทุกโมดูล
- มีการตั้งค่า GitHub Actions สำหรับการ release และการทดสอบ
