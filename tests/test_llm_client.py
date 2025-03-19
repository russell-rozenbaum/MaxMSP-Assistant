"""
Tests for the OpenRouter client.
"""
import pytest
from unittest.mock import patch, MagicMock
from src.llm_client import OpenRouterClient

def test_client_initialization():
    """Test client initialization with API key and default model."""
    client = OpenRouterClient(api_key="test_key")
    assert client.api_key == "test_key"
    assert client.model == "google/gemini-2.0-flash-lite-001"
    assert client.base_url == "https://openrouter.ai/api/v1"
    assert "Authorization" in client.headers
    assert "Content-Type" in client.headers

def test_client_initialization_with_custom_model():
    """Test client initialization with custom model."""
    custom_model = "anthropic/claude-3-sonnet"
    client = OpenRouterClient(api_key="test_key", model=custom_model)
    assert client.model == custom_model

def test_client_initialization_without_key():
    """Test client initialization without API key."""
    with pytest.raises(ValueError):
        OpenRouterClient()

@patch('requests.post')
def test_analyze_patch(mock_post):
    """Test patch analysis API call."""
    # Mock the API response
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "choices": [{
            "message": {
                "content": "Test suggestion"
            }
        }]
    }
    mock_post.return_value = mock_response
    
    # Create client and make request
    client = OpenRouterClient(api_key="test_key")
    response = client.analyze_patch("Test patch description")
    
    # Verify the API call
    mock_post.assert_called_once()
    call_args = mock_post.call_args[1]
    assert "headers" in call_args
    assert "json" in call_args
    assert call_args["json"]["model"] == "google/gemini-2.0-flash-lite-001"
    
    # Verify the response
    assert response == mock_response.json.return_value 