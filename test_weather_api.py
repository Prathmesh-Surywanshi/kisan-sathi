"""
Test script for weather API integration
Tests the new /api/weather endpoint
"""

import requests
import json

BASE_URL = "http://localhost:5000"

# Test cities
test_cities = [
    "Mumbai",
    "Delhi",
    "Bangalore",
    "Pune",
    "Chennai"
]

print("="*70)
print("TESTING WEATHER API INTEGRATION")
print("="*70)
print("\nMake sure Flask backend is running: python app.py\n")

for city in test_cities:
    try:
        print(f"Testing: {city}")
        response = requests.get(
            f"{BASE_URL}/api/weather",
            params={"city": city},
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            if data['status'] == 'success':
                weather = data['weather_data']
                print(f"  ✓ Status: {data['status']}")
                print(f"    - Temperature: {weather['temperature']}°C")
                print(f"    - Humidity: {weather['humidity']}%")
                print(f"    - Rainfall: {weather['rainfall']}cm")
                print(f"    - Condition: {weather['condition']}")
            else:
                print(f"  ✗ Error: {data.get('message', 'Unknown error')}")
        else:
            print(f"  ✗ HTTP {response.status_code}")
        
        print()
    
    except requests.exceptions.ConnectionError:
        print(f"  ✗ Cannot connect to Flask server")
        print(f"     Make sure to run: python app.py")
        break
    except Exception as e:
        print(f"  ✗ Error: {e}\n")

print("="*70)
print("✅ Weather API test complete!\n")
print("Frontend integration:")
print("1. User enters city name (e.g., 'Mumbai')")
print("2. Clicks 'Search' button")
print("3. System fetches real-time weather data")
print("4. Temperature, Humidity, Rainfall auto-fill")
print("5. User still gets soil defaults by state/district")
print("6. All together → Better crop recommendations!")
print("="*70)
