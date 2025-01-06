# API Documentation

## External APIs Used

### 1. OpenWeatherMap API
- Purpose: Weather data
- Endpoint: api.openweathermap.org/data/2.5/weather
- Documentation: https://openweathermap.org/api

### 2. IQAir API
- Purpose: Air quality data
- Endpoint: api.airvisual.com/v2
- Documentation: https://www.iqair.com/us/air-pollution-data-api

### 3. Nutritionix API
- Purpose: Nutrition data
- Endpoint: trackapi.nutritionix.com/v2
- Documentation: https://developer.nutritionix.com/

## Internal API Structure

### DataCollector
Methods for fetching external data:
- get_weather_data(location: str)
- get_air_quality(location: str)
- get_health_metrics()
- get_nutrition_data(query: str) 