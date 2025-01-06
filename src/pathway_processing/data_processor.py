import pathway as pw
from typing import Dict, Any
import json

class HealthDataProcessor:
    def __init__(self):
        self.context = pw.Context()

    def process_health_data(self, data: Dict[str, Any]) -> pw.Table:
        # Create input table from health metrics
        health_stream = self.context.table_from_pandas(
            pd.DataFrame([data])
        )

        # Process health metrics
        processed = health_stream.select(
            heart_rate=pw.this.heart_rate.value,
            spo2=pw.this.spo2.value,
            steps=pw.this.steps.current,
            sleep_score=pw.this.sleep.quality_score
        )

        return processed

    def process_environmental_data(self, weather: Dict, air: Dict) -> pw.Table:
        # Combine and process weather and air quality data
        env_data = {
            "temperature": weather["temperature"],
            "humidity": weather["humidity"],
            "aqi": air["aqi"]
        }
        
        env_stream = self.context.table_from_pandas(
            pd.DataFrame([env_data])
        )

        return env_stream 