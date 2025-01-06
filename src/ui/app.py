import streamlit as st
from datetime import datetime
import os
import asyncio
from dotenv import load_dotenv
from src.ui.components.recommendations import HealthRecommendations
from src.ui.components.advanced_charts import AdvancedCharts
from src.ui.components.health_metrics import HealthMetricsVisualizer
from src.ui.components.charts import HealthCharts
from src.data.collector import DataCollector

# Load environment variables
load_dotenv()

async def main():
    st.title("🏥 Health & Environment Monitor")
    
    # Initialize components and data collector
    recommendations = HealthRecommendations()
    charts = AdvancedCharts()
    health_viz = HealthMetricsVisualizer()
    health_charts = HealthCharts()
    data_collector = DataCollector()
    
    # Initialize session state
    if 'weather_data' not in st.session_state:
        st.session_state.weather_data = None
    if 'air_data' not in st.session_state:
        st.session_state.air_data = None
    if 'health_metrics' not in st.session_state:
        st.session_state.health_metrics = None
    if 'nutrition_data' not in st.session_state:
        st.session_state.nutrition_data = None
    
    # Create tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "Weather & Air Quality",
        "Health Metrics", 
        "Nutrition",
        "AI Recommendations"
    ])
    
    with tab1:
        st.header("🌤️ Weather & Air Quality")
        
        # Input row
        location = st.text_input("Enter Location", "London")
        if st.button("Update Weather & Air Quality", key="weather_btn"):
            try:
                with st.spinner("Fetching latest data..."):
                    weather_data = await data_collector.get_weather_data(location)
                    air_data = await data_collector.get_air_quality(location)
                    st.session_state.weather_data = weather_data
                    st.session_state.air_data = air_data
                st.success("Data updated successfully!")
            except Exception as e:
                st.error(f"Error updating data: {str(e)}")
        
        # Create two columns with better ratio
        col1, col2 = st.columns([2, 1])
        
        with col1:
            if st.session_state.weather_data:
                st.subheader("Weather Forecast")
                st.plotly_chart(
                    charts.create_weather_chart(st.session_state.weather_data),
                    use_container_width=True
                )
        
        with col2:
            if st.session_state.air_data:
                st.subheader("Air Quality")
                # AQI Gauge
                st.plotly_chart(
                    charts.create_air_quality_chart(st.session_state.air_data),
                    use_container_width=True
                )
                
                # Pollutant levels
                st.markdown("#### Pollutant Levels")
                pollutants = st.session_state.air_data['pollutants']
                if pollutants:
                    cols = st.columns(2)
                    for i, (name, value) in enumerate(pollutants.items()):
                        with cols[i % 2]:
                            if value != "N/A":
                                st.metric(
                                    name.upper(), 
                                    f"{value:.1f} µg/m³"
                                )
                else:
                    st.info("No pollutant data available")
    
    with tab2:
        st.header("💓 Health Metrics")
        col1, col2 = st.columns([2, 1])
        
        with col1:
            if st.button("Update Health Metrics", key="health_btn"):
                try:
                    with st.spinner("Fetching health metrics..."):
                        metrics = await data_collector.get_health_metrics()
                        st.session_state.health_metrics = metrics
                    st.success("Health metrics updated!")
                except Exception as e:
                    st.error(f"Error fetching health metrics: {str(e)}")
            
            if st.session_state.health_metrics:
                metrics = st.session_state.health_metrics
                metrics_cols = st.columns(3)
                
                with metrics_cols[0]:
                    st.metric("Heart Rate", 
                             f"{metrics['heart_rate']['value']} bpm")
                    st.metric("SpO₂", 
                             f"{metrics['spo2']['value']}%")
                
                with metrics_cols[1]:
                    st.metric("Steps",
                             metrics['steps']['current'],
                             f"Goal: {metrics['steps']['goal']}")
                    st.metric("Active Minutes",
                             metrics['activity']['active_minutes'])
                
                with metrics_cols[2]:
                    st.metric("Sleep Score",
                             f"{metrics['sleep']['score']}/100")
                    st.metric("Total Sleep",
                             f"{metrics['sleep']['total_hours']}h")
                
                # Show health metrics history
                st.plotly_chart(
                    charts.create_activity_timeline(metrics['activity']),
                    use_container_width=True
                )
        
        with col2:
            if st.session_state.health_metrics:
                st.plotly_chart(
                    health_viz.create_heart_rate_gauge(
                        st.session_state.health_metrics['heart_rate']
                    ),
                    use_container_width=True
                )
                
                st.plotly_chart(
                    health_viz.create_sleep_chart(
                        st.session_state.health_metrics['sleep']
                    ),
                    use_container_width=True
                )
    
    with tab3:
        st.header("🍎 Nutrition Tracker")
        col1, col2 = st.columns([3, 1])
        
        with col1:
            food_query = st.text_input("Enter food item", "1 apple", key="food_input")
            
            if st.button("Analyze", key="nutrition_btn"):
                try:
                    with st.spinner("Analyzing nutrition data..."):
                        nutrition = await data_collector.get_nutrition_data(food_query)
                        st.session_state.nutrition_data = nutrition
                    st.success("Nutrition data analyzed!")
                except Exception as e:
                    st.error(f"Error analyzing nutrition: {str(e)}")
            
            if st.session_state.nutrition_data:
                macro_cols = st.columns(4)
                with macro_cols[0]:
                    st.metric("Calories", f"{st.session_state.nutrition_data['calories']} kcal")
                with macro_cols[1]:
                    st.metric("Protein", f"{st.session_state.nutrition_data['protein']}g")
                with macro_cols[2]:
                    st.metric("Carbs", f"{st.session_state.nutrition_data['carbs']}g")
                with macro_cols[3]:
                    st.metric("Fat", f"{st.session_state.nutrition_data['fat']}g")
                
                st.plotly_chart(
                    charts.create_macro_chart(st.session_state.nutrition_data),
                    use_container_width=True
                )
    
    with tab4:
        st.header("🤖 AI Health Recommendations")
        
        if (st.session_state.weather_data and 
            st.session_state.air_data and 
            st.session_state.health_metrics):
            
            await recommendations.show_recommendations(
                st.session_state.weather_data,
                st.session_state.air_data,
                st.session_state.health_metrics
            )
        else:
            missing_data = []
            if not st.session_state.weather_data:
                missing_data.append("Weather")
            if not st.session_state.air_data:
                missing_data.append("Air Quality")
            if not st.session_state.health_metrics:
                missing_data.append("Health Metrics")
            
            st.info(f"Please update the following data first: {', '.join(missing_data)}")
            
            cols = st.columns(3)
            with cols[0]:
                if "Weather" in missing_data and st.button("Update Weather"):
                    try:
                        with st.spinner("Fetching weather data..."):
                            weather_data = await data_collector.get_weather_data("London")
                            st.session_state.weather_data = weather_data
                            st.success("Weather data updated!")
                    except Exception as e:
                        st.error(f"Error fetching weather data: {str(e)}")
            
            with cols[1]:
                if "Air Quality" in missing_data and st.button("Update Air Quality"):
                    try:
                        with st.spinner("Fetching air quality data..."):
                            air_data = await data_collector.get_air_quality("London")
                            st.session_state.air_data = air_data
                            st.success("Air quality data updated!")
                    except Exception as e:
                        st.error(f"Error fetching air quality data: {str(e)}")
            
            with cols[2]:
                if "Health Metrics" in missing_data and st.button("Update Health Metrics"):
                    try:
                        with st.spinner("Fetching health metrics..."):
                            metrics = await data_collector.get_health_metrics()
                            st.session_state.health_metrics = metrics
                            st.success("Health metrics updated!")
                    except Exception as e:
                        st.error(f"Error fetching health metrics: {str(e)}")

    # Display current time
    st.write(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    asyncio.run(main()) 