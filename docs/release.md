# 📦 คู่มือการปล่อยเวอร์ชันใหม่

## 📋 ขั้นตอนการปล่อยเวอร์ชัน

### 1. การเตรียมความพร้อม
- [ ] ตรวจสอบว่าโค้ดทั้งหมดผ่านการทดสอบ
- [ ] อัปเดต CHANGELOG.md ให้ครบถ้วน
- [ ] ตรวจสอบ dependencies ใน requirements.txt
- [ ] ตรวจสอบเวอร์ชันใน setup.py
- [ ] ตรวจสอบเอกสารทั้งหมดให้ถูกต้อง

### 2. การสร้าง Tag
```bash
# สร้าง tag ใหม่
git tag -a v1.0.0 -m "Release version 1.0.0"

# ส่ง tag ไปยัง GitHub
git push origin v1.0.0
```

### 3. การปล่อยเวอร์ชันอัตโนมัติ
- GitHub Actions จะทำงานอัตโนมัติเมื่อมีการสร้าง tag ใหม่
- ระบบจะสร้าง Release บน GitHub
- อัปโหลดไฟล์แพ็คเกจเป็น Release Asset
- (ถ้าต้องการ) เผยแพร่บน PyPI

### 4. การตรวจสอบหลังปล่อยเวอร์ชัน
- [ ] ตรวจสอบ Release บน GitHub
- [ ] ตรวจสอบ Release Assets
- [ ] ทดสอบการติดตั้งจาก PyPI (ถ้ามี)
- [ ] ตรวจสอบการทำงานของเวอร์ชันใหม่

## 🔄 การอัปเดตเวอร์ชัน

### Semantic Versioning
- **Major Version** (1.0.0): มีการเปลี่ยนแปลงที่ไม่เข้ากันกับเวอร์ชันเก่า
- **Minor Version** (0.1.0): เพิ่มฟีเจอร์ใหม่แต่ยังเข้ากันได้กับเวอร์ชันเก่า
- **Patch Version** (0.0.1): แก้ไขข้อผิดพลาดและปรับปรุงเล็กน้อย

### การอัปเดตไฟล์ที่เกี่ยวข้อง
1. `setup.py`:
```python
version="1.0.0"
```

2. `CHANGELOG.md`:
```markdown
## [0.0.1] - 2024-04-29
```

## 🚨 ข้อควรระวัง

### ก่อนปล่อยเวอร์ชัน
- ตรวจสอบการทดสอบทั้งหมดผ่าน
- ตรวจสอบความปลอดภัยของ dependencies
- ตรวจสอบการทำงานบนทุกแพลตฟอร์ม

### หลังปล่อยเวอร์ชัน
- ติดตามการรายงานปัญหา
- เตรียมพร้อมสำหรับการแก้ไขข้อผิดพลาดฉุกเฉิน
- อัปเดตเอกสารที่เกี่ยวข้อง

## 📝 การเขียน Release Notes

### โครงสร้าง Release Notes
```markdown
## [เวอร์ชัน] - วันที่

### เพิ่มใหม่
- รายการฟีเจอร์ใหม่

### การปรับปรุง
- รายการการปรับปรุง

### การแก้ไขข้อผิดพลาด
- รายการข้อผิดพลาดที่แก้ไข

### ความเข้ากันได้
- ข้อมูลเกี่ยวกับความเข้ากันได้

### เอกสาร
- การอัปเดตเอกสาร

### ความปลอดภัย
- การอัปเดตด้านความปลอดภัย
```

## 🔧 การแก้ไขปัญหา

### ปัญหาที่พบบ่อย
1. **Tag ไม่ทริกเกอร์ GitHub Actions**
   - ตรวจสอบรูปแบบของ tag (ต้องขึ้นต้นด้วย 'v')
   - ตรวจสอบการตั้งค่า GitHub Actions

2. **การสร้างแพ็คเกจล้มเหลว**
   - ตรวจสอบ setup.py
   - ตรวจสอบ dependencies

3. **การเผยแพร่บน PyPI ล้มเหลว**
   - ตรวจสอบ API Token
   - ตรวจสอบชื่อแพ็คเกจ

## 📚 เอกสารเพิ่มเติม
- [Semantic Versioning](https://semver.org/)
- [GitHub Releases](https://docs.github.com/en/repositories/releasing-projects-on-github)
- [PyPI Publishing](https://packaging.python.org/tutorials/publishing-packages/)

# การ Release (Release)

เอกสารนี้อธิบายขั้นตอนการ release โปรเจค BMT Open Python Scripts

## การเตรียมความพร้อม

ก่อนที่จะทำการ release ต้องตรวจสอบว่าได้เตรียมความพร้อมดังนี้:

1. ตรวจสอบการตั้งค่า Configuration:
   ```python
   from bmt_scripts.configimport validate_config

   # ตรวจสอบการตั้งค่า
   if not validate_config():
       print("กรุณาตั้งค่า environment variables ให้ครบถ้วน")
       exit(1)
   ```

2. ตรวจสอบ Dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. รันเทสต์ทั้งหมด:
   ```bash
   python -m pytest
   ```

## ขั้นตอนการ Release

### 1. อัปเดตเวอร์ชัน

อัปเดตเวอร์ชันในไฟล์ `pyproject.toml`:

```toml
[tool.poetry]
name = "bmt-scripts"
version = "0.1.0"  # อัปเดตเวอร์ชันตามความเหมาะสม
```

### 2. อัปเดต Changelog

เพิ่มรายละเอียดการเปลี่ยนแปลงในไฟล์ `CHANGELOG.md`:

```markdown
# Changelog

## [0.1.0] - 2024-03-21

### Added
- เพิ่มการตั้งค่า Configuration สำหรับสคริปต์ต่างๆ
- เพิ่มการทดสอบ Configuration
- เพิ่มการทดสอบ Webcam
- เพิ่มการทดสอบ Git
- เพิ่มการทดสอบ AutoGen

### Changed
- ปรับปรุงการตั้งค่า environment variables
- ปรับปรุงการทดสอบ

### Fixed
- แก้ไขการตรวจสอบ environment variables
```

### 3. สร้าง Release Branch

```bash
git checkout -b release/v0.1.0
```

### 4. Commit การเปลี่ยนแปลง

```bash
git add .
git commit -m "Release v0.1.0"
```

### 5. สร้าง Tag

```bash
git tag -a v0.1.0 -m "Release v0.1.0"
```

### 6. Push ไปยัง Remote

```bash
git push origin release/v0.1.0
git push origin v0.1.0
```

### 7. สร้าง Release บน GitHub

1. ไปที่หน้า Releases บน GitHub
2. คลิก "Create a new release"
3. เลือก tag ที่สร้างไว้
4. กรอกรายละเอียดการ release
5. คลิก "Publish release"

### 8. อัปโหลดไปยัง PyPI

```bash
# สร้าง distribution
python -m build

# อัปโหลดไปยัง PyPI
python -m twine upload dist/*
```

## การตั้งค่า GitHub Actions

### 1. Release Workflow

สร้างไฟล์ `.github/workflows/release.yml`:

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
          python -c "from bmt_scripts.configimport validate_config; assert validate_config()"
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

### 2. การตั้งค่า Secrets

1. ไปที่หน้า Settings > Secrets and variables > Actions
2. คลิก "New repository secret"
3. เพิ่ม secrets ดังนี้:
   - `OPENAI_API_KEY`: API key สำหรับ OpenAI
   - `PYPI_API_TOKEN`: API token สำหรับ PyPI

## การตรวจสอบหลัง Release

### 1. ตรวจสอบ PyPI

ตรวจสอบว่าสามารถติดตั้งแพ็คเกจได้:

```bash
pip install bmt-scripts==0.1.0
```

### 2. ตรวจสอบการทำงาน

ทดสอบการทำงานของแพ็คเกจ:

```python
from bmt_scripts.scripts.config import get_config, validate_config

# ตรวจสอบการตั้งค่า
config = get_config()
assert validate_config()

# ทดสอบการใช้งาน
print(config["webcam"])
print(config["git"])
print(config["autogen"])
```

### 3. ตรวจสอบ Documentation

ตรวจสอบว่าเอกสารอัปเดตครบถ้วน:
- README.md
- CHANGELOG.md
- docs/
  - autogen.md
  - testing.md
  - release.md

## การแก้ไขปัญหา

### 1. กรณี Release ล้มเหลว

1. ตรวจสอบ error messages ใน GitHub Actions
2. แก้ไขปัญหาและ commit การเปลี่ยนแปลง
3. สร้าง tag ใหม่และ push
4. รัน workflow ใหม่

### 2. กรณีแพ็คเกจมีปัญหา

1. สร้าง hotfix branch
2. แก้ไขปัญหาและ commit การเปลี่ยนแปลง
3. สร้าง tag ใหม่และ push
4. รัน workflow ใหม่

## หมายเหตุ

- ตรวจสอบการตั้งค่า Configuration ก่อนทำการ release
- รันเทสต์ทั้งหมดก่อนทำการ release
- อัปเดตเอกสารให้ครบถ้วน
- ตรวจสอบการทำงานหลัง release
- เตรียมแผนการแก้ไขปัญหา
