"""
Test script for loading and analyzing the simple patch.
"""
from pathlib import Path
from src.max_patch_handler import MaxPatch

def main():
    # Load the patch
    patch = MaxPatch.from_file("tests/examples/simplePatch.maxpat")
    
    # Get all objects
    objects = patch.get_objects()
    print("\nObjects in patch:")
    for obj in objects:
        box = obj.get('box', {})
        print(f"- {box.get('maxclass', 'unknown')} ({box.get('id', 'no-id')})")
        if 'text' in box:
            print(f"  Text: {box['text']}")
    
    # Get all connections
    connections = patch.get_connections()
    print("\nConnections in patch:")
    for conn in connections:
        patchline = conn.get('patchline', {})
        source = patchline.get('source', ['unknown', 0])
        dest = patchline.get('destination', ['unknown', 0])
        print(f"- {source[0]} ({source[1]}) -> {dest[0]} ({dest[1]})")
    
    # Save a copy of the patch
    patch.save("tests/examples/simplePatch_copy.maxpat")
    print("\nSaved a copy of the patch to 'tests/examples/simplePatch_copy.maxpat'")

if __name__ == "__main__":
    main() 