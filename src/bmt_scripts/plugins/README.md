# BMT Open Python Scripts Plugins

ระบบ plugin สำหรับ BMT Open Python Scripts ช่วยให้คุณสามารถเพิ่มฟีเจอร์ใหม่เข้าไปในระบบได้อย่างง่ายดาย

## โครงสร้างของ Plugin

แต่ละ plugin ควรมีโครงสร้างดังนี้:

```
plugins/
  └── your_plugin/
      ├── main.py
      └── README.md (optional)
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

## ตัวอย่างการสร้าง Plugin

1. สร้างโฟลเดอร์ใหม่ใน `plugins/`:
```bash
mkdir -p plugins/your_plugin
```

2. สร้างไฟล์ `main.py`:
```python
import click
from rich.console import Console

console = Console()

def register(plugin_manager):
    @plugin_manager.main.command()
    def hello():
        """แสดงข้อความทักทาย"""
        console.print("[green]สวัสดีจาก plugin ของคุณ![/green]")
```

3. รันคำสั่งเพื่อดู plugin ที่ติดตั้ง:
```bash
bmtlab plugins
```

## คำแนะนำในการพัฒนา Plugin

1. **การตั้งชื่อ**: ใช้ชื่อที่สื่อความหมายและไม่ซ้ำกับ plugin อื่น
2. **การจัดการ Error**: ควรจัดการ error อย่างเหมาะสมและแสดงข้อความที่เข้าใจง่าย
3. **การ Document**: ควรเขียน documentation ที่ชัดเจนสำหรับ plugin ของคุณ
4. **การทดสอบ**: ควรเขียน test cases สำหรับฟีเจอร์หลักของ plugin

## การใช้งาน Plugin Manager

Plugin Manager มีเมธอดหลักๆ ดังนี้:

- `get_plugin(name)`: ดึง plugin ตามชื่อ
- `list_plugins()`: แสดงรายการ plugins ทั้งหมด
- `reload_plugins()`: โหลด plugins ใหม่ทั้งหมด

## ตัวอย่างการใช้งาน Plugin Manager

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