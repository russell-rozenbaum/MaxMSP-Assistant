"""
Core module for handling Max/MSP patches.
"""
import json
from pathlib import Path
from typing import Dict, Any, Optional, List, Tuple
from pydantic import BaseModel, Field

class MaxPatch(BaseModel):
    """Represents a Max/MSP patch with its metadata and contents."""
    filepath: Path
    contents: Dict[str, Any] = Field(default_factory=dict)
    
    @classmethod
    def from_file(cls, filepath: str | Path) -> 'MaxPatch':
        """Load a Max patch from a file."""
        filepath = Path(filepath)
        if not filepath.exists():
            raise FileNotFoundError(f"Max patch file not found: {filepath}")
            
        with open(filepath, 'r') as f:
            contents = json.load(f)
            
        return cls(filepath=filepath, contents=contents)
    
    def save(self, output_path: Optional[str | Path] = None) -> None:
        """Save the patch to a file."""
        if output_path is None:
            output_path = self.filepath
            
        output_path = Path(output_path)
        with open(output_path, 'w') as f:
            json.dump(self.contents, f, indent=2)
            
    def get_objects(self) -> list[Dict[str, Any]]:
        """Get all objects in the patch."""
        return self.contents.get('patcher', {}).get('boxes', [])
    
    def get_connections(self) -> list[Dict[str, Any]]:
        """Get all connections in the patch."""
        return self.contents.get('patcher', {}).get('lines', [])
    
    def get_patcher_rect(self) -> List[float]:
        """Get the patch window dimensions [x, y, width, height]."""
        rect = self.contents.get('patcher', {}).get('rect', [0.0, 0.0, 800.0, 600.0])
        return rect 