"""
AutoGen integration module

This module provides integration with Microsoft's AutoGen library for AI agents
"""

try:
    from bmt_open_python_scripts.agents.autogen.core import (
        AutoGenAgent,
        CodeAgent,
        CreativeAgent,
        ResearchAgent,
    )

    __all__ = [
        "AutoGenAgent",
        "CodeAgent",
        "ResearchAgent",
        "CreativeAgent",
    ]
except ImportError:
    # Optional agents dependencies may not be installed
    __all__ = []
