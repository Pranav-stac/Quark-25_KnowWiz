import streamlit as st
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def main():
    st.title("🏥 Health & Environment Monitor")
    
    # Display weather data
    st.header("🌤️ Weather")
    city = st.text_input("City", "London")
    
    if st.button("Get Weather"):
        api_key = os.getenv("OPENWEATHER_API_KEY")
        st.write(f"Using API key: {api_key}")
        st.write(f"Getting weather for {city}...")
        # Add weather fetching logic here
    
    # Display current time
    st.write(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main() 