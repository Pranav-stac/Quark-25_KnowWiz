from typing import Dict, List

class AdaptiveHealthRAG(HealthRAG):
    def __init__(self):
        super().__init__()
        self.alert_thresholds = {
            "heart_rate": {"high": 100, "low": 60},
            "spo2": {"low": 95},
            "aqi": {"high": 100}
        }

    async def get_adaptive_recommendation(self, health_data: Dict) -> str:
        # Check for alerts
        alerts = self._check_alerts(health_data)
        
        if alerts:
            # Prioritize urgent recommendations
            return await self._get_urgent_recommendation(alerts, health_data)
        else:
            # Regular health optimization recommendations
            return await self._get_optimization_recommendation(health_data)

    def _check_alerts(self, health_data: Dict) -> List[str]:
        alerts = []
        
        # Check vital signs
        hr = health_data['heart_rate']['value']
        if hr > self.alert_thresholds['heart_rate']['high']:
            alerts.append(f"High heart rate: {hr} bpm")
        elif hr < self.alert_thresholds['heart_rate']['low']:
            alerts.append(f"Low heart rate: {hr} bpm")
        
        # Check other metrics...
        return alerts 