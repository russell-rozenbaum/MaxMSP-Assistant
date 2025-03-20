"""
Test script for analyzing a patch using the Gemini Flash Lite model.
"""
from pathlib import Path
from src.max_patch_handler import MaxPatch
from src.llm_client import OpenRouterClient

def generate_patch_description(patch: MaxPatch) -> str:
    """Generate a human-readable description of the patch with indices."""
    objects = patch.get_objects()
    connections = patch.get_connections()
    
    description = "Patch Contents:\n\n"
    
    # Describe objects with indices
    description += "Objects (with indices):\n"
    for i, obj in enumerate(objects):
        box = obj.get('box', {})
        obj_type = box.get('maxclass', 'unknown')
        obj_id = box.get('id', 'no-id')
        description += f"[{i}] - {obj_type} ({obj_id})"
        if 'text' in box:
            description += f" with text: {box['text']}"
        description += "\n"
    
    # Describe connections with indices
    description += "\nConnections (with indices):\n"
    for i, conn in enumerate(connections):
        patchline = conn.get('patchline', {})
        source = patchline.get('source', ['unknown', 0])
        dest = patchline.get('destination', ['unknown', 0])
        description += f"[{i}] - {source[0]} ({source[1]}) -> {dest[0]} ({dest[1]})\n"
    
    # Add patch dimensions for reference
    rect = patch.get_patcher_rect()
    if rect:
        description += f"\nPatch Dimensions: {rect}"
    
    return description

def main():
    # Load the patch
    patch_path = "tests/examples/simplePatch.maxpat"
    patch = MaxPatch.from_file(patch_path)
    
    # Generate description
    description = generate_patch_description(patch)
    print("Generated patch description:")
    print(description)
    
    # Initialize LLM client with Gemini Flash Lite model
    client = OpenRouterClient(model="google/gemini-2.0-flash-lite-001")
    
    # Get suggestions
    print("\nRequesting suggestions from Gemini Flash Lite...")
    suggestions = client.analyze_patch(description)
    
    # Print each suggestion in a structured way
    print(f"\nReceived {len(suggestions)} suggestions:")
    for i, suggestion in enumerate(suggestions, 1):
        print(f"\nSuggestion {i}:")
        print(f"Type: {suggestion['type']}")
        print(f"Description: {suggestion['description']}")
        print(f"Reasoning: {suggestion['reasoning']}")
        print(f"Location: {suggestion['location']['position']} {suggestion['location']['index']}")
        print("\nProposed Changes:")
        for change in suggestion['changes']:
            print(f"\nChange Type: {change['type']}")
            print("Data:")
            print(change['data'])
    
    # Apply changes to create a new patch
    output_path = "tests/examples/simplePatch_gemini_flash_lite_suggestion.maxpat"
    if client.apply_changes_to_patch(patch_path, suggestions, output_path):
        print(f"\nSuccessfully created new patch at: {output_path}")
    else:
        print("\nFailed to apply changes to patch")

if __name__ == "__main__":
    main() 