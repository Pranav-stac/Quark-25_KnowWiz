import pytest
from src.ui.components.health_metrics import HealthMetricsVisualizer
from src.ui.components.charts import HealthCharts
from src.ui.components.nutrition import NutritionVisualizer
import plotly.graph_objects as go

@pytest.fixture
def health_viz():
    return HealthMetricsVisualizer()

@pytest.fixture
def charts():
    return HealthCharts()

@pytest.fixture
def nutrition_viz():
    return NutritionVisualizer()

def test_heart_rate_gauge(health_viz, mock_health_metrics):
    """Test heart rate gauge creation"""
    fig = health_viz.create_heart_rate_gauge(mock_health_metrics["heart_rate"])
    assert isinstance(fig, go.Figure)

def test_steps_progress(health_viz, mock_health_metrics):
    """Test steps progress chart creation"""
    fig = health_viz.create_steps_progress(mock_health_metrics["steps"])
    assert isinstance(fig, go.Figure)

def test_metric_history_chart(charts):
    """Test metric history chart creation"""
    history_data = [
        {"timestamp": "2024-01-01T12:00:00", "value": 25.0},
        {"timestamp": "2024-01-01T12:05:00", "value": 25.5}
    ]
    fig = charts.create_metric_history_chart(history_data, "Temperature", "°C")
    assert isinstance(fig, go.Figure) 