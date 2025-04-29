# การทดสอบ (Testing)

เอกสารนี้อธิบายแนวทางการทดสอบสำหรับโปรเจค BMT Open Python Scripts

## โครงสร้างการทดสอบ

โครงสร้างไฟล์ทดสอบจะอยู่ในโฟลเดอร์ `tests/` โดยมีรูปแบบดังนี้:

```
tests/
├── __init__.py
├── test_webcam_list.py
├── test_config.py
└── ... (ไฟล์ทดสอบอื่นๆ)
```

## การติดตั้ง Dependencies สำหรับการทดสอบ

1. สร้าง virtual environment:
```bash
python -m venv venv
```

2. เปิดใช้งาน virtual environment:
```bash
# สำหรับ Unix/macOS
source venv/bin/activate

# สำหรับ Windows
.\venv\Scripts\activate
```

3. ติดตั้ง dependencies:
```bash
pip install pytest pytest-mock opencv-python
```

## การรันเทสต์

คุณสามารถรันเทสต์ได้หลายวิธี:

```bash
# รันเทสต์ทั้งหมด
python -m pytest

# รันเทสต์พร้อมแสดงรายละเอียด
python -m pytest -v

# รันเทสต์เฉพาะไฟล์
python -m pytest tests/test_webcam_list.py

# รันเทสต์พร้อมแสดง coverage
python -m pytest --cov=src tests/
```

## แนวทางการเขียนเทสต์

### 1. การใช้ Fixtures

Fixtures ใช้สำหรับเตรียมสภาพแวดล้อมหรือข้อมูลที่จำเป็นสำหรับการทดสอบ ตัวอย่าง:

```python
import pytest
from scripts.config import get_config, validate_config

@pytest.fixture
def config():
    """Fixture สำหรับดึงการตั้งค่าทั้งหมด"""
    return get_config()

@pytest.fixture
def webcam_config():
    """Fixture สำหรับดึงการตั้งค่ากล้องเว็บแคม"""
    config = get_config()
    return config["webcam"]

@pytest.fixture
def git_config():
    """Fixture สำหรับดึงการตั้งค่า Git"""
    config = get_config()
    return config["git"]

@pytest.fixture
def autogen_config():
    """Fixture สำหรับดึงการตั้งค่า AutoGen"""
    config = get_config()
    return config["autogen"]
```

### 2. การทดสอบ Configuration

ตัวอย่างการทดสอบการตั้งค่า:

```python
import pytest
from scripts.config import get_config, validate_config, WEBCAM_CONFIG, GIT_CONFIG, AUTOGEN_CONFIG

def test_get_config():
    """ทดสอบฟังก์ชัน get_config"""
    config = get_config()
    
    # ตรวจสอบว่ามีการตั้งค่าทั้งหมดครบถ้วน
    assert "env_vars" in config
    assert "webcam" in config
    assert "git" in config
    assert "autogen" in config
    
    # ตรวจสอบการตั้งค่ากล้องเว็บแคม
    assert config["webcam"]["default_camera"] == 0
    assert config["webcam"]["frame_width"] == 640
    assert config["webcam"]["frame_height"] == 480
    assert config["webcam"]["fps"] == 30
    
    # ตรวจสอบการตั้งค่า Git
    assert config["git"]["max_commits"] == 10
    assert "*.log" in config["git"]["exclude_patterns"]
    assert "*.tmp" in config["git"]["exclude_patterns"]
    assert "__pycache__" in config["git"]["exclude_patterns"]
    
    # ตรวจสอบการตั้งค่า AutoGen
    assert config["autogen"]["model"] == "gpt-4"
    assert config["autogen"]["temperature"] == 0.7
    assert config["autogen"]["max_tokens"] == 2000

def test_validate_config(monkeypatch):
    """ทดสอบฟังก์ชัน validate_config"""
    # จำลองการตั้งค่า OPENAI_API_KEY
    monkeypatch.setenv("OPENAI_API_KEY", "test-api-key")
    
    # ตรวจสอบว่าการตั้งค่าถูกต้อง
    assert validate_config() is True
    
    # จำลองการไม่ตั้งค่า OPENAI_API_KEY
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    
    # ตรวจสอบว่าการตั้งค่าไม่ถูกต้อง
    assert validate_config() is False
```

### 3. การทดสอบ Webcam

ตัวอย่างการทดสอบสคริปต์กล้องเว็บแคม:

```python
import pytest
from unittest.mock import patch, MagicMock
from scripts.webcam.list import list_cameras
from scripts.config import WEBCAM_CONFIG

def test_list_cameras():
    """ทดสอบฟังก์ชัน list_cameras"""
    # จำลองการทำงานของ cv2.VideoCapture
    with patch("cv2.VideoCapture") as mock_video_capture:
        # จำลองว่ามีกล้อง 2 ตัว
        mock_video_capture.return_value.isOpened.return_value = True
        mock_video_capture.return_value.read.return_value = (True, MagicMock())
        
        # เรียกใช้ฟังก์ชัน list_cameras
        cameras = list_cameras()
        
        # ตรวจสอบผลลัพธ์
        assert len(cameras) == 2
        assert cameras[0]["id"] == 0
        assert cameras[1]["id"] == 1

def test_show_camera(webcam_config):
    """ทดสอบฟังก์ชัน show_camera"""
    # จำลองการทำงานของ cv2.VideoCapture
    with patch("cv2.VideoCapture") as mock_video_capture:
        # จำลองว่ามีกล้อง 1 ตัว
        mock_video_capture.return_value.isOpened.return_value = True
        mock_video_capture.return_value.read.return_value = (True, MagicMock())
        
        # จำลองการทำงานของ cv2.imshow
        with patch("cv2.imshow") as mock_imshow:
            # จำลองการทำงานของ cv2.waitKey
            with patch("cv2.waitKey") as mock_wait_key:
                # จำลองการกดปุ่ม 'q' เพื่อออก
                mock_wait_key.return_value = ord('q')
                
                # เรียกใช้ฟังก์ชัน show_camera
                from scripts.webcam.show import show_camera
                show_camera(webcam_config["default_camera"])
                
                # ตรวจสอบว่ามีการเรียกใช้ cv2.imshow
                mock_imshow.assert_called()
```

### 4. การทดสอบ Git

ตัวอย่างการทดสอบสคริปต์ Git:

```python
import pytest
from unittest.mock import patch, MagicMock
from scripts.git.commit_summary import generate_commit_summary
from scripts.config import GIT_CONFIG

def test_generate_commit_summary(git_config):
    """ทดสอบฟังก์ชัน generate_commit_summary"""
    # จำลองการทำงานของ git.Repo
    with patch("git.Repo") as mock_repo:
        # จำลอง commit
        mock_commit = MagicMock()
        mock_commit.hexsha = "abc123"
        mock_commit.message = "Test commit message"
        mock_commit.author.name = "Test Author"
        mock_commit.author.email = "test@example.com"
        mock_commit.committed_datetime = MagicMock()
        
        # จำลอง repo.iter_commits
        mock_repo.return_value.iter_commits.return_value = [mock_commit] * git_config["max_commits"]
        
        # เรียกใช้ฟังก์ชัน generate_commit_summary
        summary = generate_commit_summary()
        
        # ตรวจสอบผลลัพธ์
        assert len(summary) == git_config["max_commits"]
        assert summary[0]["hash"] == "abc123"
        assert summary[0]["message"] == "Test commit message"
        assert summary[0]["author"] == "Test Author"
```

### 5. การทดสอบ AutoGen

ตัวอย่างการทดสอบ AutoGen agents:

```python
import pytest
from unittest.mock import patch, MagicMock
from lib.agents.autogen import CodeAgent, ResearchAgent, CreativeAgent
from scripts.config import AUTOGEN_CONFIG

def test_code_agent(autogen_config):
    """ทดสอบ CodeAgent"""
    # จำลองการทำงานของ OpenAI API
    with patch("openai.ChatCompletion.create") as mock_create:
        # จำลองการตอบกลับจาก OpenAI
        mock_create.return_value = MagicMock(
            choices=[MagicMock(message=MagicMock(content="def test_function(): pass"))]
        )
        
        # สร้าง CodeAgent
        code_agent = CodeAgent(api_key="test-api-key")
        
        # เรียกใช้ฟังก์ชัน write_code
        code = code_agent.write_code("เขียนฟังก์ชัน Python สำหรับทดสอบ")
        
        # ตรวจสอบผลลัพธ์
        assert "def test_function(): pass" in code
        
        # ตรวจสอบการเรียกใช้ OpenAI API
        mock_create.assert_called_with(
            model=autogen_config["model"],
            messages=MagicMock(),
            temperature=autogen_config["temperature"],
            max_tokens=autogen_config["max_tokens"]
        )

def test_research_agent(autogen_config):
    """ทดสอบ ResearchAgent"""
    # จำลองการทำงานของ OpenAI API
    with patch("openai.ChatCompletion.create") as mock_create:
        # จำลองการตอบกลับจาก OpenAI
        mock_create.return_value = MagicMock(
            choices=[MagicMock(message=MagicMock(content="ผลการวิจัย: Python เป็นภาษาที่ดี"))]
        )
        
        # สร้าง ResearchAgent
        research_agent = ResearchAgent(api_key="test-api-key")
        
        # เรียกใช้ฟังก์ชัน research
        result = research_agent.research("ประโยชน์ของ Python")
        
        # ตรวจสอบผลลัพธ์
        assert "Python เป็นภาษาที่ดี" in result
```

## การทดสอบ Integration

การทดสอบ Integration เป็นการทดสอบการทำงานร่วมกันระหว่างโมดูลต่างๆ ตัวอย่าง:

```python
import pytest
from scripts.config import get_config, validate_config
from scripts.webcam.list import list_cameras
from scripts.webcam.show import show_camera
from scripts.git.commit_summary import generate_commit_summary
from lib.agents.autogen import CodeAgent, ResearchAgent

def test_webcam_integration(webcam_config):
    """ทดสอบการทำงานร่วมกันของโมดูลกล้องเว็บแคม"""
    # จำลองการทำงานของ cv2.VideoCapture
    with patch("cv2.VideoCapture") as mock_video_capture:
        # จำลองว่ามีกล้อง 1 ตัว
        mock_video_capture.return_value.isOpened.return_value = True
        mock_video_capture.return_value.read.return_value = (True, MagicMock())
        
        # จำลองการทำงานของ cv2.imshow
        with patch("cv2.imshow") as mock_imshow:
            # จำลองการทำงานของ cv2.waitKey
            with patch("cv2.waitKey") as mock_wait_key:
                # จำลองการกดปุ่ม 'q' เพื่อออก
                mock_wait_key.return_value = ord('q')
                
                # เรียกใช้ฟังก์ชัน list_cameras
                cameras = list_cameras()
                
                # ตรวจสอบว่ามีกล้อง
                assert len(cameras) > 0
                
                # เรียกใช้ฟังก์ชัน show_camera
                show_camera(webcam_config["default_camera"])
                
                # ตรวจสอบว่ามีการเรียกใช้ cv2.imshow
                mock_imshow.assert_called()

def test_autogen_integration(autogen_config):
    """ทดสอบการทำงานร่วมกันของโมดูล AutoGen"""
    # จำลองการทำงานของ OpenAI API
    with patch("openai.ChatCompletion.create") as mock_create:
        # จำลองการตอบกลับจาก OpenAI
        mock_create.return_value = MagicMock(
            choices=[MagicMock(message=MagicMock(content="def test_function(): pass"))]
        )
        
        # สร้าง agents
        code_agent = CodeAgent(api_key="test-api-key")
        research_agent = ResearchAgent(api_key="test-api-key")
        
        # เรียกใช้ฟังก์ชัน write_code
        code = code_agent.write_code("เขียนฟังก์ชัน Python สำหรับทดสอบ")
        
        # ตรวจสอบผลลัพธ์
        assert "def test_function(): pass" in code
        
        # จำลองการตอบกลับจาก OpenAI สำหรับ research
        mock_create.return_value = MagicMock(
            choices=[MagicMock(message=MagicMock(content="ผลการวิจัย: Python เป็นภาษาที่ดี"))]
        )
        
        # เรียกใช้ฟังก์ชัน research
        result = research_agent.research("ประโยชน์ของ Python")
        
        # ตรวจสอบผลลัพธ์
        assert "Python เป็นภาษาที่ดี" in result
```

## การทดสอบ Performance

การทดสอบ Performance เป็นการทดสอบประสิทธิภาพการทำงานของโค้ด ตัวอย่าง:

```python
import pytest
import time
from scripts.config import get_config

def test_config_performance():
    """ทดสอบประสิทธิภาพการทำงานของฟังก์ชัน get_config"""
    # วัดเวลาที่ใช้ในการเรียกใช้ฟังก์ชัน get_config
    start_time = time.time()
    config = get_config()
    end_time = time.time()
    
    # ตรวจสอบว่าใช้เวลาไม่เกิน 0.1 วินาที
    assert end_time - start_time < 0.1
```

## การทดสอบ Security

การทดสอบ Security เป็นการทดสอบความปลอดภัยของโค้ด ตัวอย่าง:

```python
import pytest
from scripts.config import validate_config

def test_config_security():
    """ทดสอบความปลอดภัยของการตั้งค่า"""
    # ตรวจสอบว่าฟังก์ชัน validate_config ตรวจสอบ environment variables ที่จำเป็น
    assert validate_config() is False  # เมื่อไม่มีการตั้งค่า OPENAI_API_KEY
```

## หมายเหตุ

- การทดสอบควรครอบคลุมทุกฟังก์ชันและโมดูล
- ควรใช้ fixtures เพื่อลดการเขียนโค้ดซ้ำซ้อน
- ควรใช้ mocking เพื่อจำลองการทำงานของ external dependencies
- ควรทดสอบทั้งกรณีปกติและกรณีผิดพลาด
- ควรทดสอบการทำงานร่วมกันระหว่างโมดูลต่างๆ
- ควรทดสอบประสิทธิภาพการทำงานของโค้ด
- ควรทดสอบความปลอดภัยของโค้ด
