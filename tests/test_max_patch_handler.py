"""
Tests for the MaxPatch class.
"""
import pytest
from pathlib import Path
from src.max_patch_handler import MaxPatch

def test_load_and_save_patch(tmp_path):
    # Create a simple test patch
    test_patch = {
        "patcher": {
            "boxes": [
                {"box": {"id": "obj-1", "maxclass": "newobj", "text": "metro 1000"}}
            ],
            "lines": []
        }
    }
    
    # Save test patch to temporary file
    test_file = tmp_path / "test.maxpat"
    with open(test_file, 'w') as f:
        import json
        json.dump(test_patch, f)
    
    # Load the patch
    patch = MaxPatch.from_file(test_file)
    assert patch.filepath == test_file
    assert patch.get_objects() == test_patch["patcher"]["boxes"]
    
    # Save to a new location
    output_file = tmp_path / "output.maxpat"
    patch.save(output_file)
    assert output_file.exists()

def test_load_example_patch():
    """Test loading the example patch."""
    patch = MaxPatch.from_file("tests/examples/simplePatch.maxpat")
    objects = patch.get_objects()
    assert len(objects) > 0
    assert any(obj.get('box', {}).get('maxclass') == 'newobj' for obj in objects) 