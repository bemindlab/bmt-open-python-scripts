# 🔌 ระบบ Plugin

เอกสารนี้อธิบายระบบ plugin ของ BMT Open Python Scripts ซึ่งช่วยให้คุณสามารถเพิ่มฟีเจอร์ใหม่เข้าไปในระบบได้อย่างง่ายดาย

## 📋 สารบัญ

- [โครงสร้างของ Plugin](#โครงสร้างของ-plugin)
- [การสร้าง Plugin](#การสร้าง-plugin)
- [การใช้งาน Plugin Manager](#การใช้งาน-plugin-manager)
- [ตัวอย่างการสร้าง Plugin](#ตัวอย่างการสร้าง-plugin)
- [คำแนะนำในการพัฒนา Plugin](#คำแนะนำในการพัฒนา-plugin)
- [การทดสอบ Plugin](#การทดสอบ-plugin)
- [การแก้ไขปัญหา](#การแก้ไขปัญหา)

## โครงสร้างของ Plugin

แต่ละ plugin ควรมีโครงสร้างดังนี้:

```
plugins/
  └── your_plugin/
      ├── main.py
      ├── __init__.py (optional)
      ├── README.md (optional)
      └── tests/ (optional)
          └── test_your_plugin.py
```

ไฟล์ `main.py` ต้องมีฟังก์ชัน `register` ที่รับ parameter เป็น `plugin_manager`:

```python
def register(plugin_manager):
    """ลงทะเบียน plugin กับระบบ"""
    @plugin_manager.main.command()
    def your_command():
        """คำอธิบายคำสั่งของคุณ"""
        # โค้ดของคุณที่นี่
```

## การสร้าง Plugin

### 1. สร้างโฟลเดอร์ใหม่ใน `plugins/`:

```bash
mkdir -p plugins/your_plugin
```

### 2. สร้างไฟล์ `main.py`:

```python
import click
from rich.console import Console

console = Console()

def register(plugin_manager):
    """ลงทะเบียน plugin กับระบบ"""
    @plugin_manager.main.command()
    def hello():
        """แสดงข้อความทักทาย"""
        console.print("[green]สวัสดีจาก plugin ของคุณ![/green]")
```

### 3. รันคำสั่งเพื่อดู plugin ที่ติดตั้ง:

```bash
bmtlab plugins
```

## การใช้งาน Plugin Manager

Plugin Manager มีเมธอดหลักๆ ดังนี้:

- `get_plugin(name)`: ดึง plugin ตามชื่อ
- `list_plugins()`: แสดงรายการ plugins ทั้งหมด
- `reload_plugins()`: โหลด plugins ใหม่ทั้งหมด

### ตัวอย่างการใช้งาน Plugin Manager

```python
from bmt_scripts.plugins.plugin_manager import PluginManager

# สร้าง instance ของ PluginManager
plugin_manager = PluginManager()

# ดึง plugin ตามชื่อ
my_plugin = plugin_manager.get_plugin("my_plugin")

# แสดงรายการ plugins
plugins = plugin_manager.list_plugins()

# โหลด plugins ใหม่
plugin_manager.reload_plugins()
```

## ตัวอย่างการสร้าง Plugin

### 1. Plugin สำหรับการจัดการไฟล์

```python
import os
import click
from rich.console import Console
from pathlib import Path

console = Console()

def register(plugin_manager):
    """ลงทะเบียน plugin สำหรับการจัดการไฟล์"""
    
    @plugin_manager.main.group()
    def files():
        """คำสั่งสำหรับการจัดการไฟล์"""
        pass
    
    @files.command()
    @click.argument('path')
    def list(path):
        """แสดงรายการไฟล์ในโฟลเดอร์"""
        try:
            path_obj = Path(path)
            if not path_obj.exists():
                console.print(f"[red]ไม่พบโฟลเดอร์: {path}[/red]")
                return
                
            console.print(f"[bold green]รายการไฟล์ใน {path}:[/bold green]")
            for item in path_obj.iterdir():
                if item.is_file():
                    console.print(f"  📄 {item.name}")
                elif item.is_dir():
                    console.print(f"  📁 {item.name}")
        except Exception as e:
            console.print(f"[red]เกิดข้อผิดพลาด: {str(e)}[/red]")
    
    @files.command()
    @click.argument('source')
    @click.argument('destination')
    def copy(source, destination):
        """คัดลอกไฟล์จาก source ไปยัง destination"""
        try:
            import shutil
            shutil.copy2(source, destination)
            console.print(f"[green]คัดลอกไฟล์จาก {source} ไปยัง {destination} สำเร็จ[/green]")
        except Exception as e:
            console.print(f"[red]เกิดข้อผิดพลาด: {str(e)}[/red]")
```

### 2. Plugin สำหรับการจัดการฐานข้อมูล

```python
import click
from rich.console import Console
import sqlite3
import json

console = Console()

def register(plugin_manager):
    """ลงทะเบียน plugin สำหรับการจัดการฐานข้อมูล"""
    
    @plugin_manager.main.group()
    def db():
        """คำสั่งสำหรับการจัดการฐานข้อมูล"""
        pass
    
    @db.command()
    @click.argument('db_path')
    def init(db_path):
        """สร้างฐานข้อมูล SQLite ใหม่"""
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # สร้างตารางตัวอย่าง
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL
            )
            ''')
            
            conn.commit()
            conn.close()
            
            console.print(f"[green]สร้างฐานข้อมูล {db_path} สำเร็จ[/green]")
        except Exception as e:
            console.print(f"[red]เกิดข้อผิดพลาด: {str(e)}[/red]")
    
    @db.command()
    @click.argument('db_path')
    @click.argument('query')
    def query(db_path, query):
        """รันคำสั่ง SQL กับฐานข้อมูล"""
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            result = cursor.execute(query).fetchall()
            
            # แสดงผลลัพธ์
            console.print(f"[bold green]ผลลัพธ์:[/bold green]")
            for row in result:
                console.print(f"  {row}")
                
            conn.close()
        except Exception as e:
            console.print(f"[red]เกิดข้อผิดพลาด: {str(e)}[/red]")
```

## คำแนะนำในการพัฒนา Plugin

1. **การตั้งชื่อ**: ใช้ชื่อที่สื่อความหมายและไม่ซ้ำกับ plugin อื่น
2. **การจัดการ Error**: ควรจัดการ error อย่างเหมาะสมและแสดงข้อความที่เข้าใจง่าย
3. **การ Document**: ควรเขียน documentation ที่ชัดเจนสำหรับ plugin ของคุณ
4. **การทดสอบ**: ควรเขียน test cases สำหรับฟีเจอร์หลักของ plugin

## การทดสอบ Plugin

### 1. สร้างไฟล์ทดสอบ

```python
# tests/test_your_plugin.py
import pytest
from unittest.mock import patch, MagicMock
from bmt_scripts.plugins.plugin_manager import PluginManager

def test_plugin_registration():
    """ทดสอบการลงทะเบียน plugin"""
    # จำลองการทำงานของ plugin
    with patch("bmt_scripts.plugins.your_plugin.register") as mock_register:
        # สร้าง PluginManager
        plugin_manager = PluginManager()
        
        # ตรวจสอบว่ามีการเรียกใช้ฟังก์ชัน register
        mock_register.assert_called_once_with(plugin_manager)

def test_plugin_command():
    """ทดสอบคำสั่งของ plugin"""
    # จำลองการทำงานของคำสั่ง
    with patch("click.Context.invoke") as mock_invoke:
        # จำลองการรันคำสั่ง
        mock_invoke.return_value = None
        
        # ตรวจสอบผลลัพธ์
        assert mock_invoke.call_count == 1
```

### 2. รันเทสต์

```bash
# รันเทสต์เฉพาะ plugin
python -m pytest tests/test_your_plugin.py

# รันเทสต์ทั้งหมด
python -m pytest
```

## การแก้ไขปัญหา

### 1. Plugin ไม่แสดงในรายการ

- ตรวจสอบว่าไฟล์ `main.py` มีฟังก์ชัน `register`
- ตรวจสอบว่าโครงสร้างโฟลเดอร์ถูกต้อง
- ตรวจสอบ log เพื่อดูข้อผิดพลาด

### 2. คำสั่งไม่ทำงาน

- ตรวจสอบการลงทะเบียนคำสั่งในฟังก์ชัน `register`
- ตรวจสอบการใช้งาน `@plugin_manager.main.command()` ถูกต้อง
- ตรวจสอบ log เพื่อดูข้อผิดพลาด

### 3. การโหลด Plugin ใหม่

หากคุณแก้ไข plugin แล้วต้องการให้ระบบโหลดใหม่ คุณสามารถใช้คำสั่ง:

```python
from bmt_scripts.plugins.plugin_manager import PluginManager

plugin_manager = PluginManager()
plugin_manager.reload_plugins()
```

หรือรีสตาร์ทแอปพลิเคชัน 