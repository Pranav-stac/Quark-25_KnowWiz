import plotly.graph_objects as go
from datetime import datetime, timedelta
from typing import List, Dict, Any
from ...database import crud

class HealthCharts:
    def create_temperature_history(self, weather_history: List[Dict[str, Any]]) -> go.Figure:
        """Create temperature history chart from database data"""
        timestamps = [w.timestamp for w in weather_history]
        temperatures = [w.temperature for w in weather_history]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=timestamps,
            y=temperatures,
            mode='lines+markers',
            name='Temperature'
        ))
        fig.update_layout(
            title='Temperature History',
            xaxis_title='Time',
            yaxis_title='Temperature (°C)'
        )
        return fig

    def create_air_quality_history(self, air_history: List[Dict[str, Any]]) -> go.Figure:
        """Create AQI history chart from database data"""
        timestamps = [a.timestamp for a in air_history]
        aqi_values = [a.aqi for a in air_history]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=timestamps,
            y=aqi_values,
            mode='lines+markers',
            name='AQI'
        ))
        fig.update_layout(
            title='Air Quality History',
            xaxis_title='Time',
            yaxis_title='AQI'
        )
        return fig 