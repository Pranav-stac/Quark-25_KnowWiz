import aiohttp
import os
from typing import Dict, Any
from datetime import datetime, timedelta

class DataCollector:
    def __init__(self):
        self.openweather_api_key = os.getenv("OPENWEATHER_API_KEY")
        self.iqair_api_key = os.getenv("IQAIR_API_KEY")
        self.nutritionix_app_id = os.getenv("NUTRITIONIX_APP_ID")
        self.nutritionix_api_key = os.getenv("NUTRITIONIX_API_KEY")
        
        # Base URLs
        self.weather_base_url = "http://api.openweathermap.org/data/2.5"
        self.air_quality_base_url = "http://api.airvisual.com/v2"
        self.nutrition_base_url = "https://trackapi.nutritionix.com/v2"

    async def get_weather_data(self, location: str) -> Dict[str, Any]:
        """Fetch real weather data from OpenWeatherMap API"""
        if not self.openweather_api_key:
            raise ValueError("OpenWeatherMap API key not found")
        
        try:
            async with aiohttp.ClientSession() as session:
                # Current weather
                url = f"{self.weather_base_url}/weather"
                params = {
                    "q": location,
                    "appid": self.openweather_api_key,
                    "units": "metric"
                }
                
                async with session.get(url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        
                        # Also get forecast data
                        forecast_url = f"{self.weather_base_url}/forecast"
                        async with session.get(forecast_url, params=params) as forecast_response:
                            forecast_data = await forecast_response.json()
                            
                            return {
                                "temperature": data["main"]["temp"],
                                "feels_like": data["main"]["feels_like"],
                                "humidity": data["main"]["humidity"],
                                "conditions": data["weather"][0]["main"],
                                "description": data["weather"][0]["description"],
                                "wind_speed": data["wind"]["speed"],
                                "pressure": data["main"]["pressure"],
                                "icon": data["weather"][0]["icon"],
                                "forecast": [
                                    {
                                        "timestamp": item["dt"],
                                        "temp": item["main"]["temp"],
                                        "conditions": item["weather"][0]["main"],
                                        "humidity": item["main"]["humidity"]
                                    }
                                    for item in forecast_data["list"][:8]  # Next 24 hours
                                ]
                            }
                    else:
                        raise Exception(f"Weather API error: {response.status}")
        except Exception as e:
            print(f"Error fetching weather data: {str(e)}")
            raise

    async def get_air_quality(self, location: str) -> Dict[str, Any]:
        """Fetch air quality data from IQAir API"""
        if not self.iqair_api_key:
            raise ValueError("IQAir API key not found")
        
        try:
            async with aiohttp.ClientSession() as session:
                # First get location coordinates
                weather_url = f"{self.weather_base_url}/weather"
                params = {
                    "q": location,
                    "appid": self.openweather_api_key,
                    "units": "metric"
                }
                
                async with session.get(weather_url, params=params) as weather_response:
                    if weather_response.status == 200:
                        weather_data = await weather_response.json()
                        lat = weather_data['coord']['lat']
                        lon = weather_data['coord']['lon']
                        
                        # Now get air quality using coordinates
                        url = f"{self.air_quality_base_url}/nearest_city"
                        params = {
                            "key": self.iqair_api_key,
                            "lat": lat,
                            "lon": lon
                        }
                        
                        async with session.get(url, params=params) as response:
                            if response.status == 200:
                                data = await response.json()
                                current = data["data"]["current"]
                                pollution = current["pollution"]
                                
                                # Extract pollutant data with proper error handling
                                pollutants = {}
                                for pollutant in ["pm25", "pm10", "o3", "no2"]:
                                    try:
                                        value = pollution.get(pollutant, 0)
                                        if value and value != "N/A":
                                            pollutants[pollutant] = float(value)
                                    except (ValueError, TypeError):
                                        continue
                                
                                return {
                                    "aqi": pollution["aqius"],
                                    "status": self._get_aqi_status(pollution["aqius"]),
                                    "pollutants": pollutants,
                                    "temperature": current["weather"]["tp"],
                                    "humidity": current["weather"]["hu"],
                                    "wind_speed": current["weather"]["ws"],
                                    "timestamp": pollution["ts"]
                                }
                            else:
                                raise Exception(f"Air Quality API error: {response.status}")
                    else:
                        raise Exception(f"Weather API error: {weather_response.status}")
        except Exception as e:
            print(f"Error fetching air quality data: {str(e)}")
            raise

    async def get_health_metrics(self) -> Dict[str, Any]:
        """Get health metrics (mock data for demo)"""
        return {
            "heart_rate": {
                "value": 75,
                "unit": "bpm",
                "status": "Normal",
                "history": [72, 75, 73, 76, 74]
            },
            "spo2": {
                "value": 98,
                "unit": "%",
                "status": "Normal",
                "history": [98, 97, 98, 99, 98]
            },
            "steps": {
                "current": 8500,
                "goal": 10000,
                "history": [9200, 8500, 10200, 7800, 9000]
            },
            "sleep": {
                "total_hours": 7.5,
                "score": 85,
                "deep_sleep": 2.5,
                "rem_sleep": 2.0,
                "light_sleep": 3.0,
                "history": [7.2, 7.5, 8.0, 6.5, 7.5]
            },
            "activity": {
                "active_minutes": 45,
                "calories_burned": 320,
                "hourly_steps": [500, 1200, 800, 600, 900, 1500, 1000, 800]
            }
        }

    async def get_nutrition_data(self, query: str) -> Dict[str, Any]:
        """Get nutrition data from Nutritionix API"""
        if not (self.nutritionix_app_id and self.nutritionix_api_key):
            raise ValueError("Nutritionix API credentials not found")
        
        try:
            async with aiohttp.ClientSession() as session:
                url = f"{self.nutrition_base_url}/natural/nutrients"
                headers = {
                    "x-app-id": self.nutritionix_app_id,
                    "x-app-key": self.nutritionix_api_key,
                    "Content-Type": "application/json"
                }
                payload = {"query": query}
                
                async with session.post(url, json=payload, headers=headers) as response:
                    if response.status == 200:
                        data = await response.json()
                        if not data["foods"]:
                            raise ValueError("No nutrition data found for this food")
                        
                        food = data["foods"][0]
                        return {
                            "name": food["food_name"],
                            "calories": food["nf_calories"],
                            "protein": food["nf_protein"],
                            "carbs": food["nf_total_carbohydrate"],
                            "fat": food["nf_total_fat"],
                            "serving_size": f"{food['serving_qty']} {food['serving_unit']}",
                            "fiber": food["nf_dietary_fiber"],
                            "sugars": food["nf_sugars"],
                            "details": {
                                "saturated_fat": food["nf_saturated_fat"],
                                "cholesterol": food["nf_cholesterol"],
                                "sodium": food["nf_sodium"],
                                "potassium": food["nf_potassium"]
                            }
                        }
                    else:
                        raise Exception(f"Nutrition API error: {response.status}")
        except Exception as e:
            print(f"Error fetching nutrition data: {str(e)}")
            raise

    async def get_health_metrics_history(self) -> Dict[str, Any]:
        """Get historical health metrics data"""
        return {
            "timestamps": [datetime.now() - timedelta(hours=i) for i in range(24)],
            "heart_rate": [75 + i % 5 for i in range(24)],
            "steps": [1000 * i for i in range(24)],
            "active_minutes": [5 + i % 10 for i in range(24)]
        } 

    def _get_aqi_status(self, aqi: int) -> str:
        """Convert AQI number to status description"""
        if aqi <= 50:
            return "Good"
        elif aqi <= 100:
            return "Moderate"
        elif aqi <= 150:
            return "Unhealthy for Sensitive Groups"
        elif aqi <= 200:
            return "Unhealthy"
        elif aqi <= 300:
            return "Very Unhealthy"
        else:
            return "Hazardous" 