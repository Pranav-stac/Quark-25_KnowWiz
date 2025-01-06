from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Dict, Any, Optional

class UserBase(BaseModel):
    username: str
    email: EmailStr

    class Config:
        from_attributes = True

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class HealthMetricsBase(BaseModel):
    heart_rate: Dict[str, Any]
    spo2: Dict[str, Any]
    steps: Dict[str, Any]
    sleep: Dict[str, Any]
    activity: Dict[str, Any]

    class Config:
        from_attributes = True

class HealthMetricsCreate(HealthMetricsBase):
    user_id: int

class HealthMetrics(HealthMetricsBase):
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True

class WeatherDataBase(BaseModel):
    temperature: float
    humidity: int
    conditions: str
    city: str
    timestamp: datetime = datetime.utcnow()

    class Config:
        from_attributes = True

class WeatherData(WeatherDataBase):
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True

class AirQualityDataBase(BaseModel):
    aqi: int
    main_pollutant: str
    city: str
    timestamp: datetime = datetime.utcnow()

    class Config:
        from_attributes = True

class AirQualityData(AirQualityDataBase):
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True

class NutritionDataBase(BaseModel):
    food_name: str
    calories: float
    protein: float
    carbs: float
    fat: float

class NutritionDataCreate(NutritionDataBase):
    user_id: int

class NutritionData(NutritionDataBase):
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True 