import google.generativeai as genai
from typing import Dict, List
import os
from dotenv import load_dotenv

class HealthRAG:
    def __init__(self):
        load_dotenv()
        # Configure Gemini API
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        self.model = genai.GenerativeModel('gemini-pro')
        
        self.prompt_template = """
        Based on the following health data and conditions, provide personalized health recommendations:
        
        Current Conditions:
        {conditions}
        
        Please provide:
        1. Overall health assessment
        2. Specific recommendations for improvement
        3. Any precautions based on environmental conditions
        4. Activity suggestions considering all factors
        
        Keep recommendations practical and actionable.
        """

    def get_recommendation(self, query: str, health_data: Dict) -> str:
        try:
            # Format conditions for the prompt
            conditions = f"""
            Environmental:
            - Temperature: {health_data.get('weather', {}).get('temperature', 'N/A')}°C
            - Humidity: {health_data.get('weather', {}).get('humidity', 'N/A')}%
            - Weather: {health_data.get('weather', {}).get('conditions', 'N/A')}
            - Air Quality Index: {health_data.get('air_quality', {}).get('aqi', 'N/A')}
            
            Health Metrics:
            - Heart Rate: {health_data.get('health', {}).get('heart_rate', {}).get('value', 'N/A')} bpm
            - SpO₂: {health_data.get('health', {}).get('spo2', {}).get('value', 'N/A')}%
            - Sleep: {health_data.get('health', {}).get('sleep', {}).get('total_hours', 'N/A')} hours
            - Activity: {health_data.get('health', {}).get('activity', {}).get('active_minutes', 'N/A')} active minutes
            """
            
            # Generate recommendation using Gemini
            response = self.model.generate_content(
                self.prompt_template.format(conditions=conditions)
            )
            
            if not response or not response.text:
                return "Unable to generate recommendations at this time. Please try again later."
                
            return response.text.strip()
            
        except Exception as e:
            return f"Error generating recommendation: {str(e)}"

    def get_alerts(self, metrics: Dict) -> List[str]:
        """Generate health alerts based on metrics"""
        alerts = []
        
        try:
            # Check heart rate
            hr = metrics.get('heart_rate', {}).get('value')
            if hr:
                if hr > 100:
                    alerts.append("❗ High heart rate detected. Consider resting and monitoring.")
                elif hr < 60:
                    alerts.append("ℹ️ Low heart rate detected. Monitor if you're not an athlete.")
                
            # Check SpO2
            spo2 = metrics.get('spo2', {}).get('value')
            if spo2 and spo2 < 95:
                alerts.append("⚠️ Blood oxygen level is below normal. Consider deep breathing exercises.")
                
            # Check sleep
            sleep = metrics.get('sleep', {}).get('total_hours')
            if sleep and sleep < 7:
                alerts.append("😴 You're getting less than recommended sleep. Aim for 7-9 hours.")
                
            # Check activity
            activity = metrics.get('activity', {}).get('active_minutes')
            if activity and activity < 30:
                alerts.append("🏃 Low activity today. Try to get at least 30 minutes of activity.")
                
        except Exception as e:
            alerts.append(f"Error checking alerts: {str(e)}")
            
        return alerts 