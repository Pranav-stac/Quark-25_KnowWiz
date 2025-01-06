import pytest
from unittest.mock import MagicMock
import os
from dotenv import load_dotenv

load_dotenv()

@pytest.fixture
def mock_genai():
    mock_model = MagicMock()
    mock_response = MagicMock()
    mock_response.text = "Sample health recommendation"
    mock_model.generate_content.return_value = mock_response
    return mock_model

@pytest.fixture
def rag_system(mock_genai):
    from src.rag.health_rag import HealthRAG
    rag = HealthRAG()
    rag.model = mock_genai
    return rag

@pytest.fixture
def health_collector():
    from src.data_sources.health_data import HealthDataCollector
    return HealthDataCollector() 