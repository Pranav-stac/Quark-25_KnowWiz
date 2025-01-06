from typing import Callable, Any
import asyncio
from functools import wraps
import time
from .error_handling import logger, HealthMonitorException

class CircuitBreaker:
    def __init__(self, failure_threshold: int = 5, recovery_time: int = 60):
        self.failure_threshold = failure_threshold
        self.recovery_time = recovery_time
        self.failures = 0
        self.last_failure_time = 0
        self.state = "CLOSED"  # CLOSED, OPEN, HALF-OPEN

    def can_execute(self) -> bool:
        if self.state == "CLOSED":
            return True
        
        if self.state == "OPEN":
            if time.time() - self.last_failure_time >= self.recovery_time:
                self.state = "HALF-OPEN"
                return True
            return False
        
        return self.state == "HALF-OPEN"

    def record_success(self):
        self.failures = 0
        self.state = "CLOSED"

    def record_failure(self):
        self.failures += 1
        self.last_failure_time = time.time()
        
        if self.failures >= self.failure_threshold:
            self.state = "OPEN"

def retry_with_backoff(max_retries: int = 3, base_delay: float = 1):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            retries = 0
            while retries < max_retries:
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    retries += 1
                    if retries == max_retries:
                        raise
                    
                    delay = base_delay * (2 ** (retries - 1))  # Exponential backoff
                    logger.warning(f"Retry {retries}/{max_retries} after {delay}s delay", extra={
                        'error': str(e),
                        'function': func.__name__
                    })
                    await asyncio.sleep(delay)
            return None
        return wrapper
    return decorator

def with_circuit_breaker(circuit_breaker: CircuitBreaker):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            if not circuit_breaker.can_execute():
                raise HealthMonitorException(
                    message="Service temporarily unavailable",
                    error_code="CIRCUIT_BREAKER_OPEN",
                    details={'recovery_time': circuit_breaker.recovery_time}
                )
            
            try:
                result = await func(*args, **kwargs)
                circuit_breaker.record_success()
                return result
            except Exception as e:
                circuit_breaker.record_failure()
                raise
        return wrapper
    return decorator 