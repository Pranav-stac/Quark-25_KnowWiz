import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px

class HealthCharts:
    def create_aqi_gauge(self, aqi: int) -> go.Figure:
        """Create an AQI gauge chart"""
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = aqi,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Air Quality Index"},
            gauge = {
                'axis': {'range': [0, 300]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, 50], 'color': "green"},
                    {'range': [51, 100], 'color': "yellow"},
                    {'range': [101, 150], 'color': "orange"},
                    {'range': [151, 300], 'color': "red"}
                ],
            }
        ))
        return fig

    def create_weather_history(self, data: list) -> go.Figure:
        """Create weather history chart"""
        fig = make_subplots(rows=2, cols=1)
        
        # Temperature subplot
        fig.add_trace(
            go.Scatter(
                x=[d['timestamp'] for d in data],
                y=[d['temperature'] for d in data],
                name="Temperature"
            ),
            row=1, col=1
        )
        
        # Humidity subplot
        fig.add_trace(
            go.Scatter(
                x=[d['timestamp'] for d in data],
                y=[d['humidity'] for d in data],
                name="Humidity"
            ),
            row=2, col=1
        )
        
        fig.update_layout(height=600, title_text="Weather History")
        return fig 

    def create_sleep_chart(self, sleep_data: dict) -> go.Figure:
        """Create a donut chart showing sleep stages"""
        labels = ['Deep Sleep', 'Light Sleep', 'REM', 'Awake']
        values = [
            sleep_data['deep_sleep'],
            sleep_data['light_sleep'],
            sleep_data['rem'],
            sleep_data['total_hours'] - (sleep_data['deep_sleep'] + sleep_data['light_sleep'] + sleep_data['rem'])
        ]
        
        colors = ['#2E5EAA', '#5AA9E6', '#7FC8F8', '#F9F9F9']
        
        fig = go.Figure(data=[go.Pie(
            labels=labels,
            values=values,
            hole=.3,
            marker_colors=colors
        )])
        
        fig.update_layout(
            title="Sleep Stages",
            annotations=[dict(text=f"{sleep_data['total_hours']}h", x=0.5, y=0.5, font_size=20, showarrow=False)]
        )
        return fig

    def create_nutrition_chart(self, food_data: dict) -> go.Figure:
        """Create a bar chart showing macronutrients"""
        macros = ['Protein', 'Carbs', 'Fat']
        values = [food_data['protein'], food_data['carbs'], food_data['fat']]
        colors = ['#2E5EAA', '#5AA9E6', '#7FC8F8']
        
        fig = go.Figure([go.Bar(
            x=macros,
            y=values,
            marker_color=colors
        )])
        
        fig.update_layout(
            title=f"Macronutrients in {food_data['name']}",
            yaxis_title="Grams"
        )
        return fig

    def create_activity_gauge(self, activity_data: dict) -> go.Figure:
        """Create a gauge chart for activity progress"""
        fig = go.Figure(go.Indicator(
            mode = "gauge+number+delta",
            value = activity_data['active_minutes'],
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Active Minutes"},
            delta = {'reference': 30},
            gauge = {
                'axis': {'range': [None, 60]},
                'bar': {'color': "#2E5EAA"},
                'steps': [
                    {'range': [0, 30], 'color': "#F9F9F9"},
                    {'range': [30, 60], 'color': "#E8F4F8"}
                ],
                'threshold': {
                    'line': {'color': "green", 'width': 4},
                    'thickness': 0.75,
                    'value': 30
                }
            }
        ))
        return fig

    def create_health_metrics_history(self, metrics_history: list) -> go.Figure:
        """Create a line chart showing health metrics over time"""
        fig = make_subplots(rows=2, cols=2,
                           subplot_titles=("Heart Rate", "SpO₂", "Steps", "Sleep Quality"))
        
        # Heart Rate
        fig.add_trace(
            go.Scatter(
                x=[m['timestamp'] for m in metrics_history],
                y=[m['heart_rate']['value'] for m in metrics_history],
                name="Heart Rate"
            ),
            row=1, col=1
        )
        
        # SpO₂
        fig.add_trace(
            go.Scatter(
                x=[m['timestamp'] for m in metrics_history],
                y=[m['spo2']['value'] for m in metrics_history],
                name="SpO₂"
            ),
            row=1, col=2
        )
        
        # Steps
        fig.add_trace(
            go.Bar(
                x=[m['timestamp'] for m in metrics_history],
                y=[m['steps']['current'] for m in metrics_history],
                name="Steps"
            ),
            row=2, col=1
        )
        
        # Sleep Quality
        fig.add_trace(
            go.Scatter(
                x=[m['timestamp'] for m in metrics_history],
                y=[m['sleep']['quality_score'] for m in metrics_history],
                name="Sleep Quality"
            ),
            row=2, col=2
        )
        
        fig.update_layout(height=800, showlegend=False)
        return fig 