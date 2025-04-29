"""
Plugin Manager for BMT Open Python Scripts
"""

import importlib.util
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional

from bmt_scripts.config.settings import PLUGIN_CONFIG_FILE, PLUGIN_DIR

logger = logging.getLogger(__name__)


class PluginManager:
    """จัดการ plugins ของระบบ"""

    def __init__(self) -> None:
        self.plugins: Dict[str, Any] = {}
        self._load_plugins()

    def _load_plugins(self) -> None:
        """โหลด plugins ทั้งหมด"""
        if not PLUGIN_DIR.exists():
            PLUGIN_DIR.mkdir(parents=True)
            return

        for plugin_dir in PLUGIN_DIR.iterdir():
            if not plugin_dir.is_dir():
                continue

            try:
                self._load_plugin(plugin_dir)
            except Exception as e:
                logger.error(f"ไม่สามารถโหลด plugin {plugin_dir.name}: {str(e)}")

    def _load_plugin(self, plugin_dir: Path) -> None:
        """โหลด plugin จากโฟลเดอร์"""
        plugin_name = plugin_dir.name
        main_file = plugin_dir / "main.py"

        if not main_file.exists():
            logger.warning(f"ไม่พบไฟล์ main.py ใน plugin {plugin_name}")
            return

        spec = importlib.util.spec_from_file_location(plugin_name, main_file)
        if spec is None or spec.loader is None:
            raise ImportError(f"ไม่สามารถโหลด plugin {plugin_name}")

        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        if hasattr(module, "register"):
            module.register(self)
            self.plugins[plugin_name] = module
            logger.info(f"โหลด plugin {plugin_name} สำเร็จ")
        else:
            logger.warning(f"plugin {plugin_name} ไม่มีฟังก์ชัน register")

    def get_plugin(self, name: str) -> Optional[Any]:
        """ดึง plugin ตามชื่อ"""
        return self.plugins.get(name)

    def list_plugins(self) -> List[str]:
        """แสดงรายการ plugins ทั้งหมด"""
        return list(self.plugins.keys())

    def reload_plugins(self) -> None:
        """โหลด plugins ใหม่ทั้งหมด"""
        self.plugins.clear()
        self._load_plugins()
