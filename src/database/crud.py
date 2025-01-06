from sqlalchemy.orm import Session
from . import models, schemas
from datetime import datetime, timedelta
from typing import List, Optional, Dict

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(
        username=user.username,
        email=user.email
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def create_health_metrics(db: Session, metrics: schemas.HealthMetricsCreate):
    db_metrics = models.HealthMetrics(**metrics.dict())
    db.add(db_metrics)
    db.commit()
    db.refresh(db_metrics)
    return db_metrics

def get_user_health_metrics(
    db: Session, 
    user_id: int, 
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None
) -> List[models.HealthMetrics]:
    query = db.query(models.HealthMetrics).filter(models.HealthMetrics.user_id == user_id)
    
    if start_date:
        query = query.filter(models.HealthMetrics.timestamp >= start_date)
    if end_date:
        query = query.filter(models.HealthMetrics.timestamp <= end_date)
    
    return query.order_by(models.HealthMetrics.timestamp.desc()).all()

def create_weather_data(db: Session, weather: schemas.WeatherDataBase):
    db_weather = models.WeatherData(**weather.dict())
    db.add(db_weather)
    db.commit()
    db.refresh(db_weather)
    return db_weather

def get_weather_history(
    db: Session,
    hours: int = 24
) -> List[models.WeatherData]:
    start_time = datetime.utcnow() - timedelta(hours=hours)
    return db.query(models.WeatherData)\
        .filter(models.WeatherData.timestamp >= start_time)\
        .order_by(models.WeatherData.timestamp.desc())\
        .all()

def get_health_metrics_history(db: Session, hours: int = 24) -> List[Dict]:
    """Get health metrics history for the last N hours"""
    cutoff = datetime.utcnow() - timedelta(hours=hours)
    metrics = db.query(models.HealthMetrics)\
        .filter(models.HealthMetrics.timestamp >= cutoff)\
        .order_by(models.HealthMetrics.timestamp.desc())\
        .all()
    return [metric.__dict__ for metric in metrics]

def get_weather_history(db: Session, hours: int = 24) -> List[Dict]:
    """Get weather history for the last N hours"""
    cutoff = datetime.utcnow() - timedelta(hours=hours)
    weather = db.query(models.WeatherData)\
        .filter(models.WeatherData.timestamp >= cutoff)\
        .order_by(models.WeatherData.timestamp.desc())\
        .all()
    return [w.__dict__ for w in weather]

# Similar functions for air quality and nutrition data... 