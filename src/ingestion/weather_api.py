
import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")
LAT = os.getenv("LATITUDE")
LON = os.getenv("LONGITUDE")

BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


def fetch_weather():
    if not API_KEY:
        raise ValueError("OpenWeather API key is missing")

    if not LAT or not LON:
        raise ValueError("Latitude or longitude is missing")

    params = {
        "lat": LAT,
        "lon": LON,
        "appid": API_KEY,
        "units": "metric"
    }

    response = requests.get(
        BASE_URL,
        params=params,
        timeout=20
    )

    response.raise_for_status()
    data = response.json()

    weather = {
        "city": data.get("name"),
        "temperature": data["main"]["temp"],
        "feels_like": data["main"]["feels_like"],
        "humidity": data["main"]["humidity"],
        "pressure": data["main"]["pressure"],
        "weather": data["weather"][0]["description"],
        "wind_speed": data.get("wind", {}).get("speed"),
        "wind_direction": data.get("wind", {}).get("deg"),
        "cloudiness": data.get("clouds", {}).get("all"),
        "timestamp": data.get("dt")
    }

    return weather


if __name__ == "__main__":
    try:
        result = fetch_weather()

        print("\n--- Sukkur Weather ---")

        for key, value in result.items():
            print(f"{key}: {value}")

    except requests.exceptions.RequestException as error:
        print("API request failed:", error)

    except (ValueError, KeyError, IndexError) as error:
        print("Configuration or response error:", error)
