# GitHub Workflows

เอกสารนี้อธิบายเกี่ยวกับ GitHub Workflows ที่ใช้ในโปรเจค bmt-scripts

## Pre-commit Hooks

โปรเจคนี้ใช้ pre-commit hooks เพื่อตรวจสอบคุณภาพของโค้ดก่อนที่จะ commit โดยมี hooks ดังนี้:

### Code Formatting และ Style

1. **black**: จัดรูปแบบโค้ด Python ให้เป็นมาตรฐานเดียวกัน
   - Line length: 88 ตัวอักษร
   - Python version: 3.12+

2. **isort**: จัดเรียง imports ให้เป็นระเบียบ
   - ใช้ black profile
   - Multi-line output แบบที่ 3

3. **flake8**: ตรวจสอบ code style และ docstrings
   - Line length: 88 ตัวอักษร
   - ใช้ flake8-docstrings สำหรับตรวจสอบ docstrings
   - ข้ามการตรวจสอบบางอย่างตามที่กำหนดใน `.flake8`

### Type Checking

- **mypy**: ตรวจสอบ type hints ในโค้ด Python

### Security

- **bandit**: ตรวจสอบปัญหาด้านความปลอดภัยในโค้ด Python
  - ตรวจสอบเฉพาะในโฟลเดอร์ `src` และ `scripts`
  - ข้ามการตรวจสอบบางอย่างตามที่กำหนดใน `pyproject.toml`

### Code Quality

1. **pre-commit-hooks**:
   - `trailing-whitespace`: ลบช่องว่างที่ไม่จำเป็นท้ายบรรทัด
   - `end-of-file-fixer`: แก้ไขการจบไฟล์ให้ถูกต้อง
   - `check-yaml`: ตรวจสอบไฟล์ YAML
   - `check-added-large-files`: ตรวจสอบไฟล์ขนาดใหญ่
   - `check-ast`: ตรวจสอบไวยากรณ์ Python
   - `check-json`: ตรวจสอบไฟล์ JSON
   - `check-merge-conflict`: ตรวจสอบ merge conflicts
   - `detect-private-key`: ตรวจสอบ private keys ที่อาจหลุดเข้ามาในโค้ด

2. **pyupgrade**: อัพเกรดโค้ดให้ใช้ฟีเจอร์ใหม่ของ Python
   - ใช้ฟีเจอร์ของ Python 3.8+

## การติดตั้งและใช้งาน

1. ติดตั้ง pre-commit:
```bash
pip install pre-commit
```

2. ติดตั้ง pre-commit hooks:
```bash
pre-commit install
```

3. รัน pre-commit hooks กับไฟล์ทั้งหมด:
```bash
pre-commit run --all-files
```

## การแก้ไขการตั้งค่า

- การตั้งค่า pre-commit hooks อยู่ในไฟล์ `.pre-commit-config.yaml`
- การตั้งค่า black และ isort อยู่ในไฟล์ `pyproject.toml`
- การตั้งค่า flake8 อยู่ในไฟล์ `.flake8`
- การตั้งค่า bandit อยู่ในไฟล์ `pyproject.toml`

## หมายเหตุ

- pre-commit hooks จะรันอัตโนมัติเมื่อทำการ commit
- สามารถข้าม pre-commit hooks ได้โดยใช้ `git commit --no-verify` (ไม่แนะนำ)
- ควรแก้ไขปัญหาที่ pre-commit hooks ตรวจพบก่อนที่จะ commit
