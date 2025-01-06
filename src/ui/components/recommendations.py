import streamlit as st
from src.rag.health_rag import HealthRAG
from src.rag.agentic_rag import AgenticHealthRAG, AlertPriority, HealthAlert
from src.data.health_guidelines import HEALTH_GUIDELINES
from typing import Dict, List

class HealthRecommendations:
    def __init__(self):
        self.rag = HealthRAG()
        self.agentic_rag = AgenticHealthRAG()
    
    async def show_recommendations(self, weather_data: dict, air_data: dict, health_metrics: dict):
        """Display health recommendations based on current conditions"""
        try:
            # Process data and get recommendations
            recommendation, alerts = await self.agentic_rag.process_health_data({
                "weather": weather_data,
                "air_quality": air_data,
                "health": health_metrics
            })
            
            # Show current conditions summary
            with st.expander("Current Conditions Summary", expanded=True):
                self._show_conditions(weather_data, air_data, health_metrics)
            
            # Show alerts by priority
            self._show_alerts(alerts)
            
            # Show recommendations
            st.subheader("🤖 AI Health Recommendations")
            st.info(recommendation)
            
            # Show guidelines
            self._show_guidelines()
            
        except Exception as e:
            st.error(f"Error generating recommendations: {str(e)}")
    
    def _show_conditions(self, weather_data: dict, air_data: dict, health_metrics: dict):
        """Display current conditions"""
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Environmental Conditions")
            st.write(f"🌡️ Temperature: {weather_data.get('temperature', 'N/A')}°C")
            st.write(f"💧 Humidity: {weather_data.get('humidity', 'N/A')}%")
            st.write(f"☁️ Weather: {weather_data.get('conditions', 'N/A')}")
            st.write(f"🌬️ Air Quality Index: {air_data.get('aqi', 'N/A')}")
        
        with col2:
            st.subheader("Health Metrics")
            st.write(f"💓 Heart Rate: {health_metrics.get('heart_rate', {}).get('value', 'N/A')} bpm")
            st.write(f"🫁 SpO₂: {health_metrics.get('spo2', {}).get('value', 'N/A')}%")
            st.write(f"🏃 Steps: {health_metrics.get('steps', {}).get('current', 'N/A')}")
            st.write(f"😴 Sleep: {health_metrics.get('sleep', {}).get('total_hours', 'N/A')}h")
    
    def _show_alerts(self, alerts):
        """Display health alerts by priority"""
        critical_alerts = [a for a in alerts if a.priority == AlertPriority.CRITICAL]
        if critical_alerts:
            st.error("⚠️ CRITICAL ALERTS")
            for alert in critical_alerts:
                st.error(f"{alert.message} (Value: {alert.value}, Threshold: {alert.threshold})")
        
        other_alerts = [a for a in alerts if a.priority != AlertPriority.CRITICAL]
        if other_alerts:
            st.warning("⚠️ Health Alerts")
            for alert in other_alerts:
                st.warning(f"{alert.message}")
    
    def _show_guidelines(self):
        """Display health guidelines"""
        with st.expander("General Health Guidelines"):
            for category, guidelines in HEALTH_GUIDELINES.items():
                st.subheader(f"📋 {category.title()}")
                for guideline in guidelines:
                    st.write(f"• {guideline}") 