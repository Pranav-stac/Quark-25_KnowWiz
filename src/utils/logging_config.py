import logging
import logging.config
import os
from pathlib import Path
from pythonjsonlogger import jsonlogger

# Create logs directory if it doesn't exist
log_dir = Path("logs")
log_dir.mkdir(exist_ok=True)

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'json': {
            '()': 'pythonjsonlogger.jsonlogger.JsonFormatter',
            'fmt': '%(asctime)s %(levelname)s %(name)s %(message)s'
        },
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
            'level': 'INFO',
            'stream': 'ext://sys.stdout'
        },
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'json',
            'filename': os.getenv('LOG_FILE', 'logs/app.log'),
            'maxBytes': 10485760,  # 10MB
            'backupCount': 5,
            'level': 'DEBUG'
        },
        'error_file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'json',
            'filename': 'logs/error.log',
            'maxBytes': 10485760,  # 10MB
            'backupCount': 5,
            'level': 'ERROR'
        }
    },
    'loggers': {
        'health_monitor': {
            'handlers': ['console', 'file', 'error_file'],
            'level': os.getenv('LOG_LEVEL', 'INFO'),
            'propagate': False
        }
    }
}

def setup_logging():
    """Initialize logging configuration"""
    logging.config.dictConfig(LOGGING_CONFIG)
    logger = logging.getLogger('health_monitor')
    logger.info('Logging system initialized')
    return logger 