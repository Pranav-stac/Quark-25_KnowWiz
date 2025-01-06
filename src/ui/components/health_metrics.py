import plotly.graph_objects as go
from typing import Dict, Any

class HealthMetricsVisualizer:
    @staticmethod
    def create_heart_rate_gauge(heart_rate: Dict[str, Any]) -> go.Figure:
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=heart_rate["value"],
            domain={'x': [0, 1], 'y': [0, 1]},
            gauge={
                'axis': {'range': [40, 120]},
                'bar': {'color': "red"},
                'steps': [
                    {'range': [40, 60], 'color': "yellow"},
                    {'range': [60, 100], 'color': "green"},
                    {'range': [100, 120], 'color': "red"},
                ],
            },
            title={'text': f"Heart Rate ({heart_rate['status']})"}
        ))
        fig.update_layout(height=250)
        return fig
    
    @staticmethod
    def create_steps_progress(steps_data: Dict[str, Any]) -> go.Figure:
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=steps_data["current"],
            domain={'x': [0, 1], 'y': [0, 1]},
            gauge={
                'axis': {'range': [0, steps_data["goal"]]},
                'bar': {'color': "lightblue"},
                'steps': [
                    {'range': [0, steps_data["goal"]], 'color': "lightgray"}
                ],
            },
            delta={'reference': steps_data["goal"]},
            title={'text': "Daily Steps"}
        ))
        fig.update_layout(height=250)
        return fig
    
    @staticmethod
    def create_sleep_chart(sleep_data: Dict[str, Any]) -> go.Figure:
        labels = ['Deep Sleep', 'REM Sleep', 'Light Sleep']
        values = [
            sleep_data['deep_sleep'],
            sleep_data['rem_sleep'],
            sleep_data['light_sleep']
        ]
        
        fig = go.Figure(data=[go.Pie(
            labels=labels,
            values=values,
            hole=.3
        )])
        
        fig.update_layout(
            title=f"Sleep Distribution (Total: {sleep_data['total_hours']}hrs)",
            height=300
        )
        return fig 