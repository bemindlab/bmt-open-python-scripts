"""
Configuration settings for BMT Open Python Scripts
"""

import os
from pathlib import Path
from typing import Dict, Any

try:
    from dotenv import load_dotenv
    # Load environment variables from .env file
    load_dotenv()
except ImportError:
    # dotenv is optional
    pass

# Configuration for webcam scripts
WEBCAM_CONFIG = {
    "default_camera": 0,
    "frame_width": 640,
    "frame_height": 480,
    "fps": 30,
}

# Configuration for git scripts
GIT_CONFIG = {
    "max_commits": 10,
    "exclude_patterns": [
        "*.log",
        "*.tmp",
        "__pycache__",
    ],
}

# Configuration for autogen scripts
AUTOGEN_CONFIG = {
    "model": "gpt-4",
    "temperature": 0.7,
    "max_tokens": 2000,
}

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
SCRIPTS_DIR = PROJECT_ROOT / "src" / "bmt_scripts"

# Logging configuration
LOGGING_CONFIG: Dict[str, Any] = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
        },
    },
    "handlers": {
        "default": {
            "level": "INFO",
            "formatter": "standard",
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        "": {
            "handlers": ["default"],
            "level": "INFO",
            "propagate": True
        }
    }
}

# Cache configuration
CACHE_DIR = PROJECT_ROOT / ".cache"
CACHE_EXPIRY = 3600  # 1 hour in seconds

# Plugin configuration
PLUGIN_DIR = PROJECT_ROOT / "plugins"
PLUGIN_CONFIG_FILE = "plugin_config.yaml"

def get_config() -> Dict[str, Any]:
    """
    Get all configuration settings

    Returns:
        Dict[str, Any]: All configuration settings
    """
    return {
        "env_vars": {
            "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY"),
        },
        "webcam": WEBCAM_CONFIG,
        "git": GIT_CONFIG,
        "autogen": AUTOGEN_CONFIG,
    }

def validate_config() -> bool:
    """
    Validate configuration settings

    Returns:
        bool: True if configuration is valid, False otherwise
    """
    # Check environment variables
    if not os.getenv("OPENAI_API_KEY"):
        return False
    
    return True