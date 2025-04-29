# BMT Libraries

ไลบรารีและโมดูลที่ใช้ร่วมกันในโปรเจค BMT Open Python Scripts

## สารบัญ

- [BMT Libraries](#bmt-libraries)
  - [สารบัญ](#สารบัญ)
  - [โครงสร้าง](#โครงสร้าง)
  - [การใช้งาน](#การใช้งาน)
    - [1. การ Import](#1-การ-import)
    - [2. ตัวอย่างการใช้งาน](#2-ตัวอย่างการใช้งาน)
  - [แนวทางการพัฒนา](#แนวทางการพัฒนา)
    - [1. การตั้งชื่อ](#1-การตั้งชื่อ)
    - [2. เอกสาร](#2-เอกสาร)
    - [3. การจัดการข้อผิดพลาด](#3-การจัดการข้อผิดพลาด)
  - [ข้อกำหนดเพิ่มเติม](#ข้อกำหนดเพิ่มเติม)
    - [1. Dependencies](#1-dependencies)
    - [2. Performance](#2-performance)
    - [3. Security](#3-security)
  - [การทดสอบ](#การทดสอบ)
    - [1. Unit Tests](#1-unit-tests)
    - [2. Integration Tests](#2-integration-tests)
  - [การสนับสนุน](#การสนับสนุน)
  - [License](#license)

## โครงสร้าง

```
bmt_libs/
├── agents/         # โมดูลสำหรับ AI Agent
│   ├── autogen/   # AutoGen implementation
│   └── mockup/    # Mockup agent สำหรับทดสอบ
├── git/           # โมดูลสำหรับจัดการ Git
│   ├── manager.py # Git manager
│   └── models.py  # Git models
├── webcam/        # โมดูลสำหรับจัดการกล้อง
│   ├── capture.py # Webcam capture
│   └── config.py  # Webcam configuration
└── utils/         # โมดูลยูทิลิตี้ทั่วไป
    ├── logger.py  # Logging utility
    └── helpers.py # Helper functions
```

## การใช้งาน

### 1. การ Import

```python
# AutoGen Agents
from bmt_libs.agents.autogen import CodeAgent, ResearchAgent, CreativeAgent

# Git Management
from bmt_libs.git import GitManager, GitConfig

# Webcam
from bmt_libs.webcam import WebcamCapture, WebcamConfig

# Utilities
from bmt_libs.utils import logger, helpers
```

### 2. ตัวอย่างการใช้งาน

```python
# ใช้งาน AutoGen
from bmt_libs.agents.autogen import CodeAgent
code_agent = CodeAgent()
result = code_agent.write_code("เขียนฟังก์ชันคำนวณตัวเลข Fibonacci")

# ใช้งาน Git
from bmt_libs.git import GitManager
git = GitManager()
commits = git.get_recent_commits()

# ใช้งาน Webcam
from bmt_libs.webcam import WebcamCapture
webcam = WebcamCapture()
webcam.start()

# ใช้งาน Utilities
from bmt_libs.utils import logger
logger.info("เริ่มการทำงาน")
```

## แนวทางการพัฒนา

### 1. การตั้งชื่อ

- **ไฟล์และโมดูล**: ใช้ snake_case
  ```python
  # ตัวอย่าง
  webcam_capture.py
  git_manager.py
  ```

- **คลาส**: ใช้ PascalCase
  ```python
  # ตัวอย่าง
  class WebcamCapture:
      pass

  class GitManager:
      pass
  ```

- **ฟังก์ชันและตัวแปร**: ใช้ snake_case
  ```python
  # ตัวอย่าง
  def capture_frame():
      pass

  max_retries = 3
  ```

### 2. เอกสาร

- **Docstring**: ใช้รูปแบบ Google Style
  ```python
  def calculate_average(numbers: List[float]) -> float:
      """คำนวณค่าเฉลี่ยของรายการตัวเลข

      Args:
          numbers (List[float]): รายการตัวเลข

      Returns:
          float: ค่าเฉลี่ย

      Raises:
          ValueError: ถ้ารายการว่างเปล่า
      """
      if not numbers:
          raise ValueError("รายการว่างเปล่า")
      return sum(numbers) / len(numbers)
  ```

- **Type Hints**: ใช้ type hints เสมอ
  ```python
  from typing import List, Dict, Optional

  def process_data(
      data: List[Dict[str, any]],
      max_items: Optional[int] = None
  ) -> Dict[str, any]:
      pass
  ```

### 3. การจัดการข้อผิดพลาด

- **Custom Exceptions**:
  ```python
  class WebcamError(Exception):
      """ข้อผิดพลาดพื้นฐานสำหรับ Webcam"""
      pass

  class CameraNotFoundError(WebcamError):
      """ไม่พบกล้อง"""
      pass

  class PermissionError(WebcamError):
      """ไม่มีสิทธิ์เข้าถึงกล้อง"""
      pass
  ```

- **Error Handling**:
  ```python
  try:
      webcam.start()
  except CameraNotFoundError:
      logger.error("ไม่พบกล้อง")
  except PermissionError:
      logger.error("ไม่มีสิทธิ์เข้าถึงกล้อง")
  except WebcamError as e:
      logger.error(f"เกิดข้อผิดพลาด: {e}")
  ```

## ข้อกำหนดเพิ่มเติม

### 1. Dependencies

- ระบุ dependencies ใน `setup.py`:
  ```python
  setup(
      name="bmt-scripts",
      install_requires=[
          "opencv-python>=4.5.0",
          "numpy>=1.19.0",
          "rich>=10.0.0",
          "click>=8.0.0",
          "python-dotenv>=0.19.0",
          "pyautogen>=0.2.0",
      ],
      extras_require={
          "agents": ["ag2[openai]>=0.9.0"],
          "webcam": ["opencv-python>=4.5.0"],
          "git": ["gitpython>=3.1.0"],
      },
  )
  ```

### 2. Performance

- **Caching**:
  ```python
  from functools import lru_cache

  @lru_cache(maxsize=100)
  def get_cached_data(key: str) -> Dict:
      return fetch_data(key)
  ```

- **Memory Management**:
  ```python
  class ResourceManager:
      def __enter__(self):
          self.resource = allocate_resource()
          return self.resource

      def __exit__(self, exc_type, exc_val, exc_tb):
          release_resource(self.resource)
  ```

### 3. Security

- **Input Validation**:
  ```python
  def validate_input(data: Dict) -> bool:
      required_fields = ["name", "email", "age"]
      return all(field in data for field in required_fields)
  ```

- **Sensitive Data**:
  ```python
  from dotenv import load_dotenv
  import os

  load_dotenv()
  api_key = os.getenv("API_KEY")
  ```

## การทดสอบ

### 1. Unit Tests

```python
# test_webcam.py
import pytest
from bmt_libs.webcam import WebcamCapture

def test_webcam_initialization():
    webcam = WebcamCapture()
    assert webcam is not None
    assert webcam.is_initialized()

def test_webcam_capture():
    webcam = WebcamCapture()
    frame = webcam.capture_frame()
    assert frame is not None
    assert frame.shape == (480, 640, 3)
```

### 2. Integration Tests

```python
# test_integration.py
def test_webcam_git_integration():
    webcam = WebcamCapture()
    git = GitManager()

    # ถ่ายภาพ
    frame = webcam.capture_frame()

    # บันทึกภาพ
    image_path = "test_image.jpg"
    webcam.save_frame(frame, image_path)

    # Commit การเปลี่ยนแปลง
    git.add(image_path)
    commit = git.commit("เพิ่มภาพทดสอบ")

    assert commit is not None
    assert os.path.exists(image_path)
```

## การสนับสนุน

หากพบปัญหาหรือต้องการเสนอแนะการปรับปรุง:

1. **รายงานปัญหา**
   - สร้าง issue ใน [GitHub](https://github.com/bemindlab/bmt-open-python-scripts/issues)
   - อธิบายปัญหาอย่างละเอียด
   - แนบตัวอย่างโค้ดหรือ log

2. **เสนอแนะการปรับปรุง**
   - อธิบายประโยชน์ที่คาดว่าจะได้รับ
   - แนบตัวอย่างการใช้งาน
   - อธิบายแนวทางการ implement

3. **ติดต่อทีมพัฒนา**
   - Email: support@bemindlab.com
   - Discord: [Bemind Lab Community](https://discord.gg/bemindlab)

## License

โปรเจคนี้อยู่ภายใต้ MIT License - ดูรายละเอียดเพิ่มเติมได้ที่ [LICENSE](../LICENSE)
