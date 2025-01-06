import pytest
from src.data_sources.health_data import HealthDataCollector

def test_weather_data_structure(health_collector):
    """Test weather data has correct structure"""
    data = health_collector.get_weather_data("London")
    assert isinstance(data, dict)
    assert all(key in data for key in ["temperature", "humidity", "conditions", "timestamp"])
    assert isinstance(data["temperature"], (int, float))
    assert isinstance(data["humidity"], (int, float))

def test_air_quality_data_structure(health_collector):
    """Test air quality data has correct structure"""
    data = health_collector.get_air_quality()
    assert isinstance(data, dict)
    assert all(key in data for key in ["aqi", "main_pollutant", "city", "timestamp"])
    assert isinstance(data["aqi"], (int, float))

def test_nutrition_data_structure(health_collector):
    """Test nutrition data has correct structure"""
    data = health_collector.get_nutrition_data("1 apple")
    assert isinstance(data, dict)
    assert "foods" in data
    assert isinstance(data["foods"], list)
    if data["foods"]:
        food = data["foods"][0]
        assert all(key in food for key in ["name", "calories", "protein", "carbs", "fat"])

def test_health_metrics_structure(health_collector):
    """Test health metrics data has correct structure"""
    data = health_collector.get_health_metrics()
    assert isinstance(data, dict)
    assert all(key in data for key in ["heart_rate", "steps", "spo2", "sleep", "activity"]) 