from datetime import datetime, timedelta
from typing import Dict, Any, List
import aiohttp
import os
from sqlalchemy.orm import Session
from ..database import crud, schemas
from ..utils.error_handling import APIError, error_handler

class HealthDataCollector:
    def __init__(self, db: Session = None):
        self.db = db
        self.weather_api_key = os.getenv("OPENWEATHER_API_KEY")
        self.air_api_key = os.getenv("IQAIR_API_KEY")
        self.nutritionix_app_id = os.getenv("NUTRITIONIX_APP_ID")
        self.nutritionix_api_key = os.getenv("NUTRITIONIX_API_KEY")
        self._session = None

    async def setup(self):
        """Initialize the aiohttp session"""
        if not self._session:
            self._session = aiohttp.ClientSession()
        return self

    async def cleanup(self):
        """Close the aiohttp session"""
        if self._session:
            await self._session.close()
            self._session = None

    @error_handler
    async def get_weather_data(self, city: str = "London") -> Dict[str, Any]:
        """Get weather data and store in database"""
        if not self._session:
            await self.setup()

        try:
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={self.weather_api_key}&units=metric"
            async with self._session.get(url) as response:
                if response.status != 200:
                    error_text = await response.text()
                    raise APIError(f"Weather API error: {error_text}")
                data = await response.json()
            
            if "main" not in data or "weather" not in data:
                raise APIError("Invalid response from weather API")
            
            weather_data = {
                "temperature": data["main"]["temp"],
                "humidity": data["main"]["humidity"],
                "conditions": data["weather"][0]["main"],
                "city": city,
                "timestamp": datetime.utcnow()
            }
            
            if self.db:
                db_weather = crud.create_weather_data(self.db, schemas.WeatherDataBase(**weather_data))
            
            return weather_data
            
        except Exception as e:
            if isinstance(e, APIError):
                raise
            raise APIError(f"Failed to fetch weather data: {str(e)}")

    @error_handler
    async def get_weather_history(self, hours: int = 24) -> List[Dict[str, Any]]:
        """Get weather history from database"""
        return crud.get_weather_history(self.db, hours)

    @error_handler
    async def get_air_quality(self) -> Dict[str, Any]:
        """Get air quality data"""
        if not self._session:
            await self.setup()

        try:
            url = f"http://api.airvisual.com/v2/nearest_city?key={self.air_api_key}"
            async with self._session.get(url) as response:
                if response.status != 200:
                    raise APIError(f"Air Quality API error: {await response.text()}")
                data = (await response.json())["data"]
            
            air_data = {
                "aqi": data["current"]["pollution"]["aqius"],
                "main_pollutant": data["current"]["pollution"]["mainus"],
                "city": data["city"],
                "timestamp": datetime.utcnow()
            }
            
            if self.db:
                db_air = crud.create_air_quality_data(self.db, schemas.AirQualityDataBase(**air_data))
            
            return air_data
        except Exception as e:
            raise APIError(f"Failed to fetch air quality data: {str(e)}")

    @error_handler
    async def get_health_metrics(self, user_id: int = None) -> Dict[str, Any]:
        """Simulate getting health metrics from a wearable device"""
        # In a real app, this would connect to a wearable device API
        metrics = {
            "heart_rate": {
                "value": 75,
                "unit": "bpm",
                "status": "Normal",
                "timestamp": datetime.utcnow()
            },
            "spo2": {
                "value": 98,
                "unit": "%",
                "status": "Normal",
                "timestamp": datetime.utcnow()
            },
            "steps": {
                "current": 8500,
                "goal": 10000,
                "percentage": 85.0,
                "timestamp": datetime.utcnow()
            },
            "sleep": {
                "total_hours": 7.5,
                "deep_sleep": 2.5,
                "light_sleep": 4.0,
                "rem": 1.0,
                "quality_score": 85,
                "timestamp": datetime.utcnow()
            },
            "activity": {
                "active_minutes": 45,
                "calories_burned": 350,
                "timestamp": datetime.utcnow()
            }
        }
        
        if self.db and user_id:
            db_metrics = crud.create_health_metrics(
                self.db, 
                schemas.HealthMetricsCreate(user_id=user_id, **metrics)
            )
        
        return metrics

    @error_handler
    async def get_nutrition_data(self, query: str) -> Dict[str, Any]:
        """Get nutrition data for a food query"""
        url = "https://trackapi.nutritionix.com/v2/natural/nutrients"
        headers = {
            "x-app-id": self.nutritionix_app_id,
            "x-app-key": self.nutritionix_api_key,
            "Content-Type": "application/json"
        }
        data = {"query": query}
        
        if not self._session:
            self._session = aiohttp.ClientSession()
            
        async with self._session.post(url, json=data, headers=headers) as response:
            foods = (await response.json())["foods"]
        
        return {
            "foods": [{
                "name": food["food_name"],
                "calories": food["nf_calories"],
                "protein": food["nf_protein"],
                "carbs": food["nf_total_carbohydrate"],
                "fat": food["nf_total_fat"]
            } for food in foods],
            "timestamp": datetime.utcnow()
        }

    @error_handler
    async def get_health_metrics_history(self, hours: int = 24) -> List[Dict[str, Any]]:
        """Get health metrics history"""
        if self.db:
            return crud.get_health_metrics_history(self.db, hours)
        
        # Return simulated data if no database
        history = []
        current_time = datetime.utcnow()
        for i in range(hours):
            timestamp = current_time - timedelta(hours=i)
            history.append({
                'timestamp': timestamp,
                'heart_rate': {'value': 70 + (i % 10)},
                'spo2': {'value': 97 + (i % 3)},
                'steps': {'current': 8000 + (i * 100)},
                'sleep': {'quality_score': 80 + (i % 10)}
            })
        return history

    # Similar updates for air_quality and nutrition methods... 