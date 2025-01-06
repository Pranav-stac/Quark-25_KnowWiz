import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from typing import Dict, List, Any
import pandas as pd
from datetime import datetime
from plotly.subplots import make_subplots

class AdvancedCharts:
    def create_weather_chart(self, weather_data: Dict[str, Any]) -> go.Figure:
        """Create comprehensive weather visualization with stacked layout"""
        # Create figure with secondary y-axis
        fig = make_subplots(
            rows=2, cols=1,
            specs=[[{"type": "indicator"}],
                   [{"type": "scatter"}]],
            row_heights=[0.4, 0.6],
            vertical_spacing=0.15
        )

        # Temperature gauge in top subplot
        fig.add_trace(
            go.Indicator(
                mode="gauge+number+delta",
                value=weather_data["temperature"],
                delta={"reference": weather_data["feels_like"]},
                title={"text": f"Temperature (°C)<br><span style='font-size:0.8em'>{weather_data['description']}</span>"},
                gauge={
                    "axis": {"range": [-10, 40]},
                    "bar": {"color": "orange"},
                    "steps": [
                        {"range": [-10, 0], "color": "lightblue"},
                        {"range": [0, 15], "color": "lightyellow"},
                        {"range": [15, 25], "color": "lightgreen"},
                        {"range": [25, 40], "color": "pink"}
                    ]
                }
            ),
            row=1, col=1
        )

        # Forecast timeline in bottom subplot
        if weather_data.get("forecast"):
            timestamps = [datetime.fromtimestamp(item["timestamp"]).strftime('%H:%M') 
                         for item in weather_data["forecast"]]
            temps = [item["temp"] for item in weather_data["forecast"]]
            conditions = [item["conditions"] for item in weather_data["forecast"]]
            
            fig.add_trace(
                go.Scatter(
                    x=timestamps,
                    y=temps,
                    name="Temperature",
                    mode="lines+markers",
                    text=conditions,
                    hovertemplate="<b>%{text}</b><br>" +
                                 "Time: %{x}<br>" +
                                 "Temperature: %{y}°C<br>" +
                                 "<extra></extra>",
                    line=dict(color='royalblue')
                ),
                row=2, col=1
            )

        # Update layout
        fig.update_layout(
            height=600,  # Increased height for better spacing
            margin=dict(t=60, b=40, l=40, r=40),
            showlegend=True,
            plot_bgcolor='white',
            paper_bgcolor='white'
        )

        # Update axes for forecast subplot
        fig.update_xaxes(
            title="Time",
            showgrid=True,
            row=2, col=1
        )
        fig.update_yaxes(
            title="Temperature (°C)",
            showgrid=True,
            row=2, col=1
        )

        return fig

    def create_air_quality_chart(self, air_data: Dict[str, Any]) -> go.Figure:
        """Create air quality visualization"""
        fig = go.Figure()

        # AQI gauge
        fig.add_trace(go.Indicator(
            mode="gauge+number",
            value=air_data["aqi"],
            title={
                "text": f"Air Quality Index<br><span style='font-size:0.8em;color:gray'>{air_data['status']}</span>",
                "font": {"size": 16}
            },
            domain={"x": [0, 1], "y": [0, 1]},
            gauge={
                "axis": {"range": [0, 300], "tickwidth": 1},
                "bar": {"color": "darkblue"},
                "bgcolor": "white",
                "steps": [
                    {"range": [0, 50], "color": "lightgreen"},
                    {"range": [51, 100], "color": "yellow"},
                    {"range": [101, 150], "color": "orange"},
                    {"range": [151, 200], "color": "red"},
                    {"range": [201, 300], "color": "purple"}
                ],
                "threshold": {
                    "line": {"color": "red", "width": 4},
                    "thickness": 0.75,
                    "value": air_data["aqi"]
                }
            }
        ))

        fig.update_layout(
            height=250,  # Reduced height
            margin=dict(t=60, b=20, l=20, r=20),  # Adjusted margins
            paper_bgcolor='white',
            font={"color": "darkblue"}
        )
        return fig

    def create_nutrition_chart(self, nutrition_data: Dict[str, Any]) -> go.Figure:
        """Create nutrition breakdown chart"""
        # Calculate macronutrient calories
        macros = {
            "Protein": nutrition_data["protein"] * 4,  # 4 calories per gram
            "Carbs": nutrition_data["carbs"] * 4,      # 4 calories per gram
            "Fat": nutrition_data["fat"] * 9           # 9 calories per gram
        }
        
        # Create pie chart
        fig = go.Figure(data=[
            go.Pie(
                labels=list(macros.keys()),
                values=list(macros.values()),
                hole=.3,
                marker_colors=['#FF9999', '#66B2FF', '#99FF99']
            )
        ])
        
        # Add total calories in center
        fig.add_annotation(
            text=f"{nutrition_data['calories']:.0f}\nkcal",
            x=0.5, y=0.5,
            font_size=20,
            showarrow=False
        )
        
        fig.update_layout(
            title=f"Nutrition Breakdown - {nutrition_data['name']}",
            height=400
        )
        
        return fig

    def create_health_metrics_chart(self, metrics: Dict[str, Any]) -> go.Figure:
        """Create health metrics visualization"""
        fig = go.Figure()
        
        # Heart rate gauge
        fig.add_trace(go.Indicator(
            mode="gauge+number",
            value=metrics["heart_rate"]["value"],
            domain={"x": [0, 0.5], "y": [0, 0.5]},
            title={"text": "Heart Rate (BPM)"},
            gauge={
                "axis": {"range": [40, 120]},
                "bar": {"color": "red"},
                "steps": [
                    {"range": [40, 60], "color": "yellow"},
                    {"range": [60, 100], "color": "lightgreen"},
                    {"range": [100, 120], "color": "red"}
                ]
            }
        ))
        
        # SpO2 gauge
        fig.add_trace(go.Indicator(
            mode="gauge+number",
            value=metrics["spo2"]["value"],
            domain={"x": [0.5, 1], "y": [0, 0.5]},
            title={"text": "SpO₂ (%)"},
            gauge={
                "axis": {"range": [80, 100]},
                "bar": {"color": "darkblue"},
                "steps": [
                    {"range": [80, 90], "color": "red"},
                    {"range": [90, 95], "color": "yellow"},
                    {"range": [95, 100], "color": "lightgreen"}
                ]
            }
        ))
        
        # Steps progress
        fig.add_trace(go.Indicator(
            mode="gauge+number+delta",
            value=metrics["steps"]["current"],
            domain={"x": [0, 1], "y": [0.5, 1]},
            delta={"reference": metrics["steps"]["goal"]},
            title={"text": "Daily Steps"},
            gauge={
                "axis": {"range": [0, metrics["steps"]["goal"]]},
                "bar": {"color": "lightblue"},
                "steps": [
                    {"range": [0, metrics["steps"]["goal"]], "color": "lightgray"}
                ]
            }
        ))
        
        fig.update_layout(height=600)
        return fig

    def create_activity_timeline(self, activity_data: Dict[str, Any]) -> go.Figure:
        """Create activity timeline visualization"""
        # Ensure we have hourly_steps data
        if 'hourly_steps' not in activity_data:
            return go.Figure()  # Return empty figure if no data
        
        # Create DataFrame with matching lengths
        df = pd.DataFrame({
            'Hour': list(range(len(activity_data['hourly_steps']))),  # Match length of steps
            'Steps': activity_data['hourly_steps']
        })
        
        fig = go.Figure()
        
        # Add steps bars
        fig.add_trace(go.Bar(
            x=df['Hour'],
            y=df['Steps'],
            name='Steps',
            marker_color='lightblue'
        ))
        
        # Add target line - make sure it matches the length
        target = 500  # Example target
        fig.add_trace(go.Scatter(
            x=df['Hour'],
            y=[target] * len(df['Hour']),  # Match length of hours
            name='Target',
            line=dict(color='red', dash='dash')
        ))
        
        fig.update_layout(
            title="Hourly Activity",
            xaxis_title="Hour",
            yaxis_title="Steps",
            height=300,
            showlegend=True,
            barmode='overlay'
        )
        
        return fig 

    def create_macro_chart(self, nutrition_data: Dict[str, Any]) -> go.Figure:
        """Create macronutrient breakdown chart"""
        # Extract macronutrients
        macros = {
            'Protein': nutrition_data['protein'],
            'Carbs': nutrition_data['carbs'],
            'Fat': nutrition_data['fat']
        }
        
        # Calculate total calories from each macro
        calories = {
            'Protein': macros['Protein'] * 4,  # 4 cal/g
            'Carbs': macros['Carbs'] * 4,      # 4 cal/g
            'Fat': macros['Fat'] * 9           # 9 cal/g
        }
        
        # Create donut chart
        fig = go.Figure(data=[go.Pie(
            labels=list(macros.keys()),
            values=list(calories.values()),
            hole=.4,
            textinfo='label+percent',
            marker_colors=['#FF9999', '#66B2FF', '#99FF99']
        )])
        
        # Add total calories in center
        fig.add_annotation(
            text=f"{nutrition_data['calories']:.0f}<br>kcal",
            x=0.5, y=0.5,
            font=dict(size=20),
            showarrow=False
        )
        
        fig.update_layout(
            title=f"Macronutrient Breakdown - {nutrition_data['name']}",
            height=400,
            showlegend=True
        )
        
        return fig 