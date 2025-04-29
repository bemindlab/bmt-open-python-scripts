# 📚 BMT Open Python Scripts Documentation

เอกสารสำหรับโปรเจค BMT Open Python Scripts ซึ่งเป็นชุดเครื่องมือสำหรับการทำงานกับ hardware และการจัดการโปรเจค

## 📋 สารบัญ

### 📖 เอกสารหลัก
- [โครงสร้างโปรเจค](project-structure.md) - โครงสร้างและองค์ประกอบของโปรเจค
- [การทดสอบ](testing.md) - วิธีการทดสอบและเขียน test cases
- [การ Release](release.md) - ขั้นตอนการ release เวอร์ชันใหม่
- [ระบบ Plugin](plugins.md) - วิธีการสร้างและใช้งาน plugin
- [AutoGen](autogen.md) - การใช้งาน AutoGen สำหรับ agent scripts
- [GitHub Workflows](github-workflows.md) - การตั้งค่า CI/CD และ workflows

### 🚀 เริ่มต้นใช้งาน

1. ติดตั้งโปรเจค:
```bash
pip install -e .
```

2. ทดสอบการติดตั้ง:
```bash
bmtlab --version
```

3. ดูคำสั่งที่มีทั้งหมด:
```bash
bmtlab --help
```

### 👩‍💻 คู่มือสำหรับนักพัฒนา

1. **การเพิ่มฟีเจอร์ใหม่**
   - สร้าง plugin ใหม่ตาม [เอกสารระบบ Plugin](plugins.md)
   - เขียน test cases ตาม [เอกสารการทดสอบ](testing.md)
   - อัปเดต documentation ที่เกี่ยวข้อง

2. **การทดสอบ**
## 📝 การอัปเดตเอกสาร

เมื่อมีการเพิ่มหรือแก้ไขเอกสาร กรุณาอัปเดตสารบัญในไฟล์นี้ด้วย

## 🔍 การค้นหาเอกสาร

คุณสามารถค้นหาเอกสารได้โดยใช้คำค้นหาใน GitHub หรือใช้เครื่องมือค้นหาในโปรเจค
