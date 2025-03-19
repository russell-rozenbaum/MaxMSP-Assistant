# Max/MSP Patch Handler

A Python library for handling Max/MSP patches, with a focus on automation and programmatic manipulation of patch files.

## Project Structure

```
max-msp-assistant/
├── src/                    # Source code
│   └── max_patch_handler.py
├── tests/                  # Test files
│   ├── __init__.py
│   ├── test_max_patch_handler.py
│   └── test_simple_patch.py
├── examples/              # Example Max patches
│   └── simplePatch.maxpat
├── requirements.txt
└── README.md
```

## Features

- Load and save Max/MSP patch files (.maxpat)
- Access patch objects and connections
- Basic patch manipulation capabilities

## Installation

1. Clone this repository
2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

```python
from src.max_patch_handler import MaxPatch

# Load a patch
patch = MaxPatch.from_file("examples/patch.maxpat")

# Get all objects in the patch
objects = patch.get_objects()

# Get all connections
connections = patch.get_connections()

# Save the patch to a new location
patch.save("examples/output.maxpat")
```

## Development

To run tests:

```bash
pytest tests/
```

To analyze an example patch:

```bash
python tests/test_simple_patch.py
```

## License

MIT License
