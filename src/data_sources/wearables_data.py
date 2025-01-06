import random
from datetime import datetime, timedelta
from typing import Dict, List, Any
from faker import Faker

fake = Faker()

class WearablesDataCollector:
    def __init__(self):
        self.last_heart_rate = 70  # Starting heart rate
        self.last_steps = 0
        self.last_spo2 = 98
        self.daily_step_goal = 10000
        
    def get_heart_rate(self) -> Dict[str, Any]:
        """Simulate heart rate data with realistic variations"""
        # Simulate small random changes in heart rate
        change = random.uniform(-5, 5)
        self.last_heart_rate = max(40, min(120, self.last_heart_rate + change))
        
        return {
            "value": round(self.last_heart_rate, 1),
            "unit": "bpm",
            "timestamp": datetime.now().isoformat(),
            "status": self._get_heart_rate_status(self.last_heart_rate)
        }
    
    def get_steps_data(self) -> Dict[str, Any]:
        """Simulate step count data"""
        # Simulate step increases
        new_steps = random.randint(0, 100)  # Random steps since last check
        self.last_steps += new_steps
        
        return {
            "current": self.last_steps,
            "goal": self.daily_step_goal,
            "percentage": (self.last_steps / self.daily_step_goal) * 100,
            "timestamp": datetime.now().isoformat()
        }
    
    def get_spo2_data(self) -> Dict[str, Any]:
        """Simulate SpO₂ data"""
        # Simulate small variations in SpO₂
        change = random.uniform(-1, 1)
        self.last_spo2 = max(90, min(100, self.last_spo2 + change))
        
        return {
            "value": round(self.last_spo2, 1),
            "unit": "%",
            "timestamp": datetime.now().isoformat(),
            "status": self._get_spo2_status(self.last_spo2)
        }
    
    def get_sleep_data(self) -> Dict[str, Any]:
        """Simulate sleep data for last night"""
        total_sleep = random.uniform(6, 9)  # Hours
        deep_sleep = total_sleep * random.uniform(0.2, 0.3)
        rem_sleep = total_sleep * random.uniform(0.2, 0.25)
        light_sleep = total_sleep - deep_sleep - rem_sleep
        
        return {
            "total_hours": round(total_sleep, 1),
            "deep_sleep": round(deep_sleep, 1),
            "rem_sleep": round(rem_sleep, 1),
            "light_sleep": round(light_sleep, 1),
            "quality_score": random.randint(50, 100),
            "timestamp": (datetime.now() - timedelta(hours=8)).isoformat()
        }
    
    def get_activity_data(self) -> Dict[str, Any]:
        """Simulate activity data"""
        return {
            "active_minutes": random.randint(0, 60),
            "calories_burned": random.randint(1500, 3000),
            "distance": round(random.uniform(0, 5), 2),
            "floors_climbed": random.randint(0, 20),
            "timestamp": datetime.now().isoformat()
        }
    
    @staticmethod
    def _get_heart_rate_status(hr: float) -> str:
        if hr < 60:
            return "Low"
        elif hr < 100:
            return "Normal"
        else:
            return "High"
    
    @staticmethod
    def _get_spo2_status(spo2: float) -> str:
        if spo2 >= 95:
            return "Normal"
        elif spo2 >= 90:
            return "Concerning"
        else:
            return "Low"

    def reset_daily_data(self):
        """Reset daily counters (call this at midnight)"""
        self.last_steps = 0 