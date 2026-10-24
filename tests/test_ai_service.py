from unittest.mock import MagicMock
import pytest

from src.capabilities.tools import lookup_course
from src.config import config
from src.models.model_client import (
    ModelClientError,
    OllamaConnectionError,
    ModelNotFoundError,
)
from src.services.ai_service import AIService, generate_response


def test_config_loading():
    """Verify that configuration settings load expected string values from environment or defaults."""
    assert config.ollama_base_url is not None
    assert config.model_name is not None
    assert isinstance(config.ollama_base_url, str)
    assert isinstance(config.model_name, str)


def test_empty_input_validation():
    """Verify that empty or whitespace inputs are rejected gracefully without invoking the model."""
    mock_client = MagicMock()
    service = AIService(model_client=mock_client)

    # Test empty string
    response_empty = service.process_message("")
    assert response_empty.success is False
    assert "Please enter a message" in response_empty.content
    assert mock_client.generate.call_count == 0

    # Test whitespace string
    response_spaces = service.process_message("   ")
    assert response_spaces.success is False
    assert mock_client.generate.call_count == 0


def test_successful_response_generation():
    """Verify that valid input invokes model client and returns the generated string response."""
    mock_client = MagicMock()
    mock_client.generate.return_value = "Hello! I am an AI assistant."
    service = AIService(model_client=mock_client)

    result_text = generate_response("Hello, AI", service=service)

    assert result_text == "Hello! I am an AI assistant."
    mock_client.generate.assert_called_once_with("Hello, AI")


def test_ollama_connection_error_handling():
    """Verify that Ollama connection failures produce a friendly application-level error message."""
    mock_client = MagicMock()
    mock_client.generate.side_effect = OllamaConnectionError("Connection refused at http://localhost:11434")
    service = AIService(model_client=mock_client)

    response = service.process_message("Test message")

    assert response.success is False
    assert "Could not connect to Ollama" in response.content
    assert "Connection refused" in response.error_message


def test_model_not_found_error_handling():
    """Verify that missing model exceptions are converted into controlled user messages."""
    mock_client = MagicMock()
    mock_client.generate.side_effect = ModelNotFoundError("Model llama3.2 not found locally")
    service = AIService(model_client=mock_client)

    response = service.process_message("Test message")

    assert response.success is False
    assert "configured AI model is unavailable" in response.content
    assert "llama3.2 not found" in response.error_message


# ---------------------------------------------------------------------------
# Course lookup tool tests (no Ollama needed)
# ---------------------------------------------------------------------------


def test_lookup_course_found():
    """Verify that a known course and activity returns the stored deadline."""
    result = lookup_course("SAMPLE-AI", "project")

    assert result.found is True
    assert result.deadline == "2026-10-30T16:00:00+02:00"


def test_lookup_course_not_found():
    """Verify that an unknown course returns found=False and no invented deadline."""
    result = lookup_course("UNKNOWN-1", "project")

    assert result.found is False
    assert result.deadline is None


def test_lookup_course_rejects_invalid_activity():
    """Verify that strict validation rejects activities other than workshop/project."""
    with pytest.raises(Exception):
        lookup_course("SAMPLE-AI", "exam")