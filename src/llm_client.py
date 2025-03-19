"""
Client for interacting with OpenRouter API for LLM-based patch analysis.
"""
import os
import re
import json
from pathlib import Path
import requests
from typing import Dict, Any, Optional, List, Tuple
from dotenv import load_dotenv

class OpenRouterClient:
    """Client for making API calls to OpenRouter."""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "google/gemini-2.0-flash-lite-001"):
        """
        Initialize the client with an API key and model.
        
        Args:
            api_key: OpenRouter API key
            model: Model to use for analysis (default: google/gemini-2.0-flash-lite-001)
        """
        load_dotenv()  # Load environment variables from .env file
        self.api_key = api_key or os.getenv('OPENROUTER_API_KEY')
        if not self.api_key:
            raise ValueError("OpenRouter API key is required")
        
        self.base_url = "https://openrouter.ai/api/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        self.model = model
    
    def _extract_json_from_response(self, text: str) -> List[Dict[str, Any]]:
        """
        Extract structured data from the response.
        
        Returns:
            List of dictionaries, each containing:
            - type: Type of suggestion
            - description: Brief description
            - reasoning: Why the change is beneficial
            - location: Where to insert the changes (index-based)
            - changes: List of changes in Max/MSP JSON format
        """
        suggestions = []
        
        # Split the text into individual suggestions
        # Each suggestion starts with TYPE: and ends before the next TYPE: or end of text
        suggestion_texts = re.split(r'(?=TYPE:)', text.strip())
        
        for suggestion_text in suggestion_texts:
            if not suggestion_text.strip():
                continue
                
            # Extract type, description, reasoning, and location
            type_match = re.search(r'TYPE:\s*(\w+)', suggestion_text)
            desc_match = re.search(r'DESCRIPTION:\s*(.+?)(?:\n|$)', suggestion_text)
            reason_match = re.search(r'REASONING:\s*(.+?)(?:\n|$)', suggestion_text)
            location_match = re.search(r'LOCATION:\s*(\w+)\s+(\d+)', suggestion_text)
            
            # Extract JSON changes
            json_match = re.search(r'```json\n(.*?)```', suggestion_text, re.DOTALL)
            
            if not all([type_match, desc_match, reason_match, location_match, json_match]):
                print(f"Warning: Skipping malformed suggestion:\n{suggestion_text}")
                continue
                
            try:
                changes = json.loads(json_match.group(1))
            except (json.JSONDecodeError, AttributeError):
                print(f"Warning: Invalid JSON in suggestion:\n{suggestion_text}")
                continue
                
            suggestions.append({
                "type": type_match.group(1),
                "description": desc_match.group(1).strip(),
                "reasoning": reason_match.group(1).strip(),
                "location": {
                    "position": location_match.group(1),
                    "index": int(location_match.group(2))
                },
                "changes": changes
            })
        
        if not suggestions:
            raise ValueError("No valid suggestions found in response")
            
        return suggestions
    
    def _adjust_coordinates(self, box: Dict[str, Any], reference_box: Dict[str, Any], position: str) -> Dict[str, Any]:
        """Adjust coordinates of a new box based on reference box and position."""
        ref_rect = reference_box['box']['patching_rect']
        new_rect = box['box']['patching_rect']
        
        if position == 'BEFORE':
            # Place above the reference box
            new_rect[1] = ref_rect[1] - 50  # 50 units above
            new_rect[0] = ref_rect[0]  # Same x coordinate
        elif position == 'AFTER':
            # Place below the reference box
            new_rect[1] = ref_rect[1] + 50  # 50 units below
            new_rect[0] = ref_rect[0]  # Same x coordinate
            
        box['box']['patching_rect'] = new_rect
        return box
    
    def apply_changes_to_patch(self, patch_path: str, suggestions: List[Dict[str, Any]], output_path: str) -> bool:
        """
        Apply multiple suggested changes to a patch file.
        
        Args:
            patch_path: Path to the original patch file
            suggestions: List of dictionaries containing suggestions and changes
            output_path: Path where to save the modified patch
            
        Returns:
            bool: True if changes were applied successfully
        """
        # Read the original patch
        with open(patch_path, 'r') as f:
            patch_data = json.load(f)
        
        # Get the boxes array
        boxes = patch_data['patcher']['boxes']
        
        # Sort suggestions by index to process them in order
        sorted_suggestions = sorted(suggestions, key=lambda x: x['location']['index'])
        
        # Track how many items we've inserted to adjust subsequent indices
        total_inserted = 0
        
        # Process each suggestion
        for suggestion in sorted_suggestions:
            # Get reference index for positioning
            ref_index = suggestion['location']['index']
            if ref_index >= len(boxes):
                print(f"Warning: Reference index {ref_index} is out of range")
                ref_index = len(boxes) - 1
            
            # Adjust the reference index based on previous insertions
            adjusted_ref_index = ref_index + total_inserted
            
            # Determine insertion index based on position
            position = suggestion['location']['position']
            if position == 'BEFORE':
                insert_index = adjusted_ref_index
            elif position == 'AFTER':
                insert_index = adjusted_ref_index + 1
            else:
                print(f"Warning: Unknown position {position}, defaulting to AFTER")
                insert_index = adjusted_ref_index + 1
            
            # Add new objects at the correct position in the array
            for change in suggestion['changes']:
                if change['type'] == 'add_object':
                    # Insert the new box at the determined position
                    boxes.insert(insert_index, change['data'])
                    insert_index += 1  # Move to next position for multiple objects
                    total_inserted += 1  # Track total insertions
                elif change['type'] == 'add_connection':
                    # Add the new connection to the lines array
                    patch_data['patcher']['lines'].append(change['data'])
        
        # Write the modified patch
        with open(output_path, 'w') as f:
            json.dump(patch_data, f, indent=2)
            
        return True
    
    def analyze_patch(self, patch_text: str) -> Dict[str, Any]:
        """
        Analyze a Max/MSP patch and generate a suggestion.
        
        Args:
            patch_text: Textual description of the patch
            
        Returns:
            Dictionary containing:
            - type: Type of suggestion
            - description: Brief description
            - reasoning: Why the change is beneficial
            - location: Where to insert the changes (index-based)
            - changes: List of changes in Max/MSP JSON format
        """
        # Load the prompt template
        prompt_path = Path(__file__).parent / "prompts" / "patch_analysis.txt"
        with open(prompt_path, 'r') as f:
            prompt_template = f.read()
        
        # Format the prompt
        prompt = prompt_template.format(patch_text=patch_text)
        
        # Prepare the request
        payload = {
            "model": self.model,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7,
            "max_tokens": 1000
        }
        
        # Make the API call
        response = requests.post(
            f"{self.base_url}/chat/completions",
            headers=self.headers,
            json=payload
        )
        response.raise_for_status()
        
        # Extract the content from the response
        content = response.json()['choices'][0]['message']['content']
        
        # Parse and return structured data
        return self._extract_json_from_response(content) 