# Health & Environment Monitor

[![GitHub Repository](https://img.shields.io/badge/GitHub-Repository-blue?logo=github)](https://github.com/Pranav-stac/Quark-25_KnowWiz)
[![Live Demo](https://img.shields.io/badge/Live-Demo-green?logo=streamlit)](http://15.206.147.226:8501/)

A real-time health, weather, and environmental monitoring dashboard built with Streamlit and Python.

## Quick Links

- [GitHub Repository](https://github.com/Pranav-stac/Quark-25_KnowWiz)
- [Live Demo](http://15.206.147.226:8501/)

## Media

### Images
- [![Image 1](https://i.ibb.co/RNJwQmM/image1.png)](https://ibb.co/RNJwQmM)
- [![Image 2](https://i.ibb.co/0fKxVY1/image2.png)](https://ibb.co/0fKxVY1)
- [![Image 3](https://i.ibb.co/QDvPtJN/image3.png)](https://ibb.co/QDvPtJN)

### Video
- [Watch Video](https://vimeo.com/1044401486?share=copy)

## Features

- 🌤️ Real-time weather monitoring
  - Current weather conditions
  - Temperature and humidity tracking
  - Weather forecasts
- 💨 Air quality tracking
  - Real-time AQI monitoring
  - Detailed pollutant analysis (PM2.5, PM10, O3, NO2)
  - Air quality alerts
- 💓 Health metrics visualization
  - Heart rate monitoring
  - SpO₂ tracking
  - Step counting
  - Sleep analysis
- 🍎 Nutrition analysis
  - Food nutrition lookup
  - Macronutrient breakdown
  - Calorie tracking
- 🤖 AI-powered health recommendations
  - Personalized health insights
  - Environmental health warnings
  - Activity recommendations

## Prerequisites

- Python 3.8+
- pip (Python package manager)
- Git

## API Keys Required

You'll need to obtain API keys from:
- OpenWeatherMap: [Get API Key](https://openweathermap.org/api)
- IQAir: [Get API Key](https://www.iqair.com/air-pollution-data-api)
- Nutritionix: [Get API Key](https://www.nutritionix.com/business/api)
- Google Gemini: [Get API Key](https://makersuite.google.com/app/apikey)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/health-monitor.git
cd health-monitor
```

2. Create and activate virtual environment:
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your API keys
```

## Usage

1. Start the application:
```bash
streamlit run src/ui/app.py
```

2. Open your browser and navigate to `http://localhost:8501`

3. Use the interface to:
   - Monitor weather and air quality
   - Track health metrics
   - Analyze nutrition
   - Get AI recommendations

## Project Structure
```
health-monitor/
├── src/
│   ├── data/
│   │   ├── collector.py      # API data collection
│   │   └── __init__.py
│   ├── ui/
│   │   ├── components/
│   │   │   ├── advanced_charts.py
│   │   │   ├── charts.py
│   │   │   ├── recommendations.py
│   │   │   └── __init__.py
│   │   ├── app.py           # Main Streamlit application
│   │   └── __init__.py
│   └── rag/
│       ├── agentic_rag.py   # AI recommendations
│       └── __init__.py
├── docs/
│   ├── setup.md
│   └── api.md
├── requirements.txt
├── .env.example
└── README.md
```

## API Documentation

### External APIs

1. **OpenWeatherMap API**
- Endpoint: `api.openweathermap.org/data/2.5/weather`
- Used for: Weather data
- Parameters:
  - `q`: City name
  - `appid`: API key
  - `units`: Metric/Imperial

2. **IQAir API**
- Endpoint: `api.airvisual.com/v2/nearest_city`
- Used for: Air quality data
- Parameters:
  - `lat`, `lon`: Location coordinates
  - `key`: API key

3. **Nutritionix API**
- Endpoint: `trackapi.nutritionix.com/v2/natural/nutrients`
- Used for: Nutrition data
- Headers:
  - `x-app-id`: Application ID
  - `x-app-key`: API key

### Internal API Structure

```python
class DataCollector:
    async def get_weather_data(location: str) -> Dict
    async def get_air_quality(location: str) -> Dict
    async def get_health_metrics() -> Dict
    async def get_nutrition_data(query: str) -> Dict
```

## Deployment

### Local Deployment
1. Follow the installation steps above
2. Run with Streamlit
3. Access at `http://localhost:8501`

### Cloud Deployment (Streamlit Cloud)
1. Push code to GitHub
2. Connect to [Streamlit Cloud](https://streamlit.io/cloud)
3. Deploy from repository
4. Set environment variables in Streamlit Cloud dashboard

### Docker Deployment
1. Build image:
```bash
docker build -t health-monitor .
```

2. Run container:
```bash
docker run -p 8501:8501 health-monitor
```

## Troubleshooting

### Common Issues

1. **API Key Errors**
   - Ensure all API keys are correctly set in `.env`
   - Verify API key validity

2. **Installation Issues**
   - Update pip: `pip install --upgrade pip`
   - Install wheel: `pip install wheel`

3. **Runtime Errors**
   - Check Python version compatibility
   - Verify all dependencies are installed

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidelines.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Weather data: OpenWeatherMap
- Air quality data: IQAir
- Nutrition data: Nutritionix
- AI capabilities: Google Gemini

