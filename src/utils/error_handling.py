import logging
from typing import Dict, Any, Optional
from functools import wraps
import traceback
from pythonjsonlogger import jsonlogger
import os
from datetime import datetime

# Configure JSON logger
logger = logging.getLogger('health_monitor')
logHandler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter(
    fmt='%(asctime)s %(levelname)s %(name)s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)
logger.setLevel(os.getenv('LOG_LEVEL', 'INFO'))

# Custom exceptions
class HealthMonitorException(Exception):
    """Base exception for health monitor application"""
    def __init__(self, message: str, error_code: str, details: Optional[Dict[str, Any]] = None):
        self.message = message
        self.error_code = error_code
        self.details = details or {}
        super().__init__(self.message)

class APIError(Exception):
    """Custom exception for API errors"""
    def __init__(self, message: str, details: dict = None):
        self.message = message
        self.details = details or {}
        super().__init__(self.message)

class DataValidationError(HealthMonitorException):
    """Exception for data validation errors"""
    pass

class DatabaseError(HealthMonitorException):
    """Exception for database-related errors"""
    pass

# Error handler decorator
def error_handler(func):
    """Decorator to handle API errors"""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except APIError as e:
            logging.error(f"API Error in {func.__name__}: {str(e)}")
            raise APIError(str(e))
        except Exception as e:
            logging.error(f"Unexpected error in {func.__name__}: {str(e)}")
            raise APIError(f"An unexpected error occurred: {str(e)}")
    return wrapper

# Rate limiting decorator
def rate_limit(calls: int, period: int):
    def decorator(func):
        last_reset = datetime.now()
        calls_made = 0
        
        @wraps(func)
        async def wrapper(*args, **kwargs):
            nonlocal last_reset, calls_made
            now = datetime.now()
            
            # Reset counter if period has passed
            if (now - last_reset).seconds >= period:
                calls_made = 0
                last_reset = now
            
            # Check rate limit
            if calls_made >= calls:
                raise HealthMonitorException(
                    message="Rate limit exceeded",
                    error_code="RATE_LIMIT_EXCEEDED",
                    details={'reset_in': period - (now - last_reset).seconds}
                )
            
            calls_made += 1
            return await func(*args, **kwargs)
        return wrapper
    return decorator

# Validation decorator using Pydantic
def validate_input(model):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                validated_data = model(**kwargs)
                return await func(*args, **validated_data.dict())
            except Exception as e:
                raise DataValidationError(
                    message="Invalid input data",
                    error_code="VALIDATION_ERROR",
                    details={'errors': str(e)}
                )
        return wrapper
    return decorator 