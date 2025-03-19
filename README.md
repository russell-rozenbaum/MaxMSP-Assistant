# Max/MSP Assistant

An AI-powered assistant for Max/MSP patch development and optimization.

## Features

- Analyzes Max/MSP patches using LLM technology
- Suggests improvements to patch structure and functionality
- Automatically applies suggested changes to patches
- Handles multiple suggestions with proper index management
- Supports various types of improvements:
  - Object additions
  - Connection modifications
  - Parameter optimizations
  - Structure improvements
  - Error fixes

## Recent Updates

### Multiple Suggestion Support

- Enhanced the LLM client to handle multiple suggestions per analysis
- Implemented proper index management for sequential changes
- Improved suggestion sorting and processing

### Improved Prompt Engineering

- Refined the LLM prompt for better suggestion formatting
- Added explicit examples and format requirements
- Enhanced error handling for malformed suggestions

### Security Improvements

- Added `.env` file support for API key management
- Created `.env.example` template for developer setup
- Ensured sensitive data is properly gitignored

## Setup

1. Clone the repository
2. Copy `.env.example` to `.env` and add your OpenRouter API key:
   ```bash
   cp .env.example .env
   ```
3. Edit `.env` and replace `your_api_key_here` with your actual OpenRouter API key

## Usage

Run the test script to analyze a patch:

```bash
PYTHONPATH=. python tests/test_gemini_analysis.py
```

## Development

The project uses:

- Python 3.x
- OpenRouter API for LLM access
- JSON-based Max/MSP patch format

## License

MIT License
