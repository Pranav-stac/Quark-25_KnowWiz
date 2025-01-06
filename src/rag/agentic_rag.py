from typing import Dict, List, Tuple
from dataclasses import dataclass
from enum import Enum
import numpy as np
from src.rag.health_rag import HealthRAG

class AlertPriority(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4

@dataclass
class HealthAlert:
    message: str
    priority: AlertPriority
    metric: str
    value: float
    threshold: float

class AgenticHealthRAG(HealthRAG):
    def __init__(self):
        super().__init__()
        self.alert_thresholds = {
            "heart_rate": {
                "critical": {"high": 120, "low": 50},
                "warning": {"high": 100, "low": 60}
            },
            "spo2": {
                "critical": {"low": 92},
                "warning": {"low": 95}
            },
            "temperature": {
                "critical": {"high": 39, "low": 35},
                "warning": {"high": 37.5, "low": 36}
            }
        }
        
        # Initialize dynamic thresholds with default values
        self.dynamic_thresholds = {}
        self.alert_history = []

    async def process_health_data(self, health_data: Dict) -> Tuple[str, List[HealthAlert]]:
        """Process health data and autonomously determine actions"""
        
        # 1. Analyze data urgency and context
        alerts = self._check_critical_conditions(health_data)
        context_priority = self._determine_context_priority(health_data)
        
        # 2. Generate appropriate prompt
        if any(alert.priority == AlertPriority.CRITICAL for alert in alerts):
            prompt = self._generate_emergency_prompt(alerts)
        else:
            prompt = self._generate_standard_prompt(health_data)
        
        # 3. Get recommendation using base RAG
        recommendation = self.get_recommendation(prompt, health_data)
        
        # 4. Update dynamic thresholds based on patterns
        self._update_dynamic_thresholds(health_data)
        
        return recommendation, sorted(alerts, key=lambda x: x.priority.value, reverse=True)

    def _check_critical_conditions(self, health_data: Dict) -> List[HealthAlert]:
        """Check for critical health conditions"""
        alerts = []
        
        # Check vital signs against thresholds
        hr = health_data.get('heart_rate', {}).get('value')
        if hr:
            if hr > self.alert_thresholds['heart_rate']['critical']['high']:
                alerts.append(HealthAlert(
                    message="CRITICAL: Extremely high heart rate detected!",
                    priority=AlertPriority.CRITICAL,
                    metric="heart_rate",
                    value=hr,
                    threshold=self.alert_thresholds['heart_rate']['critical']['high']
                ))
            elif hr < self.alert_thresholds['heart_rate']['critical']['low']:
                alerts.append(HealthAlert(
                    message="CRITICAL: Extremely low heart rate detected!",
                    priority=AlertPriority.CRITICAL,
                    metric="heart_rate",
                    value=hr,
                    threshold=self.alert_thresholds['heart_rate']['critical']['low']
                ))
        
        # Add more vital sign checks...
        return alerts

    def _determine_context_priority(self, health_data: Dict) -> float:
        """Determine the priority of the current context"""
        priority_score = 0.0
        
        # Check environmental factors
        temp = health_data.get('weather', {}).get('temperature')
        if temp:
            if temp > 30 or temp < 10:
                priority_score += 0.3
        
        aqi = health_data.get('air_quality', {}).get('aqi')
        if aqi and aqi > 100:
            priority_score += 0.3
        
        # Check health metrics
        if self._has_critical_alerts(health_data):
            priority_score += 0.4
        
        return min(priority_score, 1.0)

    def _update_dynamic_thresholds(self, health_data: Dict):
        """Update thresholds based on patterns"""
        # Store historical data
        self.alert_history.append(health_data)
        if len(self.alert_history) > 100:
            self.alert_history.pop(0)
        
        # Analyze patterns and adjust thresholds
        if len(self.alert_history) >= 50:
            for metric in ['heart_rate', 'spo2']:
                values = [h.get(metric, {}).get('value') for h in self.alert_history if h.get(metric)]
                if values:
                    mean = np.mean(values)
                    std = np.std(values)
                    self.dynamic_thresholds[metric] = {
                        "high": mean + 2 * std,
                        "low": mean - 2 * std
                    } 

    def _has_critical_alerts(self, health_data: Dict) -> bool:
        """Check if there are any critical health conditions"""
        hr = health_data.get('heart_rate', {}).get('value')
        spo2 = health_data.get('spo2', {}).get('value')
        
        if hr and (hr > self.alert_thresholds['heart_rate']['critical']['high'] or 
                  hr < self.alert_thresholds['heart_rate']['critical']['low']):
            return True
            
        if spo2 and spo2 < self.alert_thresholds['spo2']['critical']['low']:
            return True
            
        return False

    def _generate_emergency_prompt(self, alerts: List[HealthAlert]) -> str:
        """Generate prompt for emergency situations"""
        critical_conditions = [
            f"{alert.metric}: {alert.value} (Threshold: {alert.threshold})"
            for alert in alerts if alert.priority == AlertPriority.CRITICAL
        ]
        
        return f"""
        EMERGENCY SITUATION DETECTED:
        {', '.join(critical_conditions)}
        
        Please provide:
        1. Immediate actions needed
        2. Emergency precautions
        3. When to seek medical attention
        4. Monitoring instructions
        
        Keep recommendations clear, concise, and focused on safety.
        """

    def _generate_standard_prompt(self, health_data: Dict) -> str:
        """Generate standard recommendation prompt"""
        return f"""
        Based on the current health metrics and conditions:
        - Heart Rate: {health_data.get('heart_rate', {}).get('value', 'N/A')} bpm
        - SpO2: {health_data.get('spo2', {}).get('value', 'N/A')}%
        - Temperature: {health_data.get('weather', {}).get('temperature', 'N/A')}°C
        - Air Quality: {health_data.get('air_quality', {}).get('aqi', 'N/A')}
        
        Please provide:
        1. Overall health assessment
        2. Personalized recommendations
        3. Activity suggestions
        4. Environmental precautions
        
        Focus on optimization and prevention.
        """ 