# Setup Guide

## Prerequisites
- Python 3.8+
- pip

## Installation
1. Clone the repository
2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Configuration
1. Get required API keys:
- Google Gemini API key
- OpenWeatherMap API key
- IQAir API key
- Nutritionix API credentials

2. Configure environment:
```bash
cp .env.example .env
# Edit .env with your API keys
```

## Running the Application
```bash
streamlit run src/ui/app.py
``` 