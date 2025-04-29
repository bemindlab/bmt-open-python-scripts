# Source Code Directory Structure

This directory contains the source code for the BMT Open Python Scripts project, organized into two main packages:

## Package Structure

```
src/
├── __init__.py             # Root package marker
├── bmt_libs/               # Library modules (internal use)
│   ├── __init__.py
│   ├── agents/             # Agent implementations 
│   │   └── autogen/        # Microsoft AutoGen libraries
│   └── hardware/           # Hardware access libraries
│       ├── camera.py
│       └── screen.py
└── bmt_scripts/            # Executable script modules
    ├── __init__.py
    ├── _version.py
    ├── agents/             # Agent scripts
    ├── config/             # Configuration
    ├── git/                # Git utilities
    ├── hardware/           # Hardware scripts
    ├── main.py             # Main entry point
    ├── plugins/            # Plugin system
    └── webcam/             # Webcam utilities
```

## Usage Guidelines

1. **bmt_libs**: Contains shared libraries that can be imported by scripts
   - Use for code that needs to be shared across multiple scripts
   - Focus on reusability and abstraction

2. **bmt_scripts**: Contains executable scripts that provide functionality
   - Each module typically has a `main()` function for CLI usage
   - Uses libraries from `bmt_libs` package

## Import Conventions

- Inter-package imports should use absolute imports:
  ```python
  # From a script importing a library
  from bmt_libs.agents.autogen.core import CodeAgent
  
  # From a library importing another library
  from bmt_libs.hardware.camera import Camera
  ```

- Intra-package imports can use relative imports:
  ```python
  # Within the same package
  from .settings import LOGGING_CONFIG
  ```

## Adding New Modules

1. For new library functionality:
   - Add to appropriate subpackage in `bmt_libs/`
   - Create `__init__.py` for new directories
   - Add unit tests in `tests/`

2. For new executable scripts:
   - Add to appropriate subpackage in `bmt_scripts/`
   - Register in `cli.py` if command-line access is needed