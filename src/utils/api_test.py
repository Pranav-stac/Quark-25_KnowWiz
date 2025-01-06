import os
import requests
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

def test_openweather_api():
    """Test OpenWeatherMap API"""
    api_key = os.getenv("OPENWEATHER_API_KEY")
    url = f"http://api.openweathermap.org/data/2.5/weather?q=London&appid={api_key}"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print("✅ OpenWeatherMap API: Success")
            return True
        else:
            print(f"❌ OpenWeatherMap API Error: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ OpenWeatherMap API Error: {str(e)}")
        return False

def test_iqair_api():
    """Test IQAir API"""
    api_key = os.getenv("IQAIR_API_KEY")
    url = f"http://api.airvisual.com/v2/nearest_city?key={api_key}"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print("✅ IQAir API: Success")
            return True
        else:
            print(f"❌ IQAir API Error: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ IQAir API Error: {str(e)}")
        return False

def test_nutritionix_api():
    """Test Nutritionix API"""
    app_id = os.getenv("NUTRITIONIX_APP_ID")
    api_key = os.getenv("NUTRITIONIX_API_KEY")
    url = "https://trackapi.nutritionix.com/v2/natural/nutrients"
    headers = {
        "x-app-id": app_id,
        "x-app-key": api_key,
        "Content-Type": "application/json"
    }
    data = {
        "query": "1 apple"
    }
    
    try:
        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 200:
            print("✅ Nutritionix API: Success")
            return True
        else:
            print(f"❌ Nutritionix API Error: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Nutritionix API Error: {str(e)}")
        return False

def test_gemini_api():
    """Test Google Gemini API"""
    api_key = os.getenv("GOOGLE_API_KEY")
    
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content("Hello!")
        print("✅ Gemini API: Success")
        return True
    except Exception as e:
        print(f"❌ Gemini API Error: {str(e)}")
        return False

def main():
    print("Testing APIs...")
    print("-" * 50)
    
    all_tests = [
        test_openweather_api(),
        test_iqair_api(),
        test_nutritionix_api(),
        test_gemini_api()
    ]
    
    print("-" * 50)
    if all(all_tests):
        print("✅ All APIs are working correctly!")
    else:
        print("❌ Some APIs failed. Please check the errors above.")

if __name__ == "__main__":
    main() 