from typing import Dict

# UI Settings
THEME_CONFIG = {
    "primary_color": "#FF4B4B",
    "background_color": "#F0F2F6",
    "secondary_background_color": "#FFFFFF",
    "text_color": "#262730",
}

# Health Guidelines
AQI_LEVELS: Dict[str, Dict] = {
    "Good": {"range": (0, 50), "color": "green"},
    "Moderate": {"range": (51, 100), "color": "yellow"},
    "Unhealthy for Sensitive Groups": {"range": (101, 150), "color": "orange"},
    "Unhealthy": {"range": (151, 200), "color": "red"},
    "Very Unhealthy": {"range": (201, 300), "color": "purple"},
    "Hazardous": {"range": (301, 500), "color": "maroon"},
}

TEMPERATURE_GUIDELINES: Dict[str, Dict] = {
    "Cold": {"range": (-float('inf'), 10), "color": "blue"},
    "Cool": {"range": (10, 20), "color": "lightblue"},
    "Comfortable": {"range": (20, 25), "color": "green"},
    "Warm": {"range": (25, 30), "color": "orange"},
    "Hot": {"range": (30, float('inf')), "color": "red"},
}

HUMIDITY_GUIDELINES: Dict[str, Dict] = {
    "Too Dry": {"range": (0, 30), "color": "red"},
    "Optimal": {"range": (30, 50), "color": "green"},
    "High": {"range": (50, 70), "color": "yellow"},
    "Too Humid": {"range": (70, 100), "color": "red"},
}

# Chart Settings
CHART_CONFIG = {
    "height": 400,
    "margin": dict(l=50, r=50, t=50, b=50),
    "template": "plotly_white",
}

# Data Collection Settings
UPDATE_INTERVAL = 300  # 5 minutes in seconds
MAX_HISTORY_POINTS = 144  # 12 hours worth of 5-minute intervals 