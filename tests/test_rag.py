import pytest
from src.rag.health_rag import HealthRAG

def test_rag_initialization(rag_system):
    """Test RAG system initializes correctly"""
    assert rag_system.llm is not None
    assert rag_system.rag is not None

def test_health_alerts(rag_system):
    """Test health alerts generation"""
    metrics = {
        "heart_rate": {"status": "High"},
        "spo2": {"status": "Normal"},
        "sleep": {"total_hours": 6, "quality_score": 80}
    }
    alerts = rag_system.get_alerts(metrics)
    assert isinstance(alerts, list)
    assert len(alerts) > 0  # Should have at least one alert for high heart rate
    # Verify specific alert content
    assert any("heart rate" in alert.lower() for alert in alerts)

def test_recommendation_generation(rag_system):
    """Test health recommendation generation"""
    context = """
    Current conditions:
    - Temperature: 25°C (Comfortable)
    - Humidity: 60%
    - Weather: Clear
    - Air Quality Index: 75 (Moderate)
    """
    recommendation = rag_system.get_recommendation(context)
    assert isinstance(recommendation, str)
    assert len(recommendation) > 0
    # Verify the mock was called with the correct context
    rag_system.rag.serve_callable.assert_called_once() 