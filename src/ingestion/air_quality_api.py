
import os
import requests
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("AQICN_API_TOKEN")
LAT = os.getenv("LATITUDE")
LON = os.getenv("LONGITUDE")

BASE_URL = "https://api.waqi.info/feed/geo:{lat};{lon}/"


def fetch_air_quality():
    if not TOKEN:
        raise ValueError("AQICN token is missing")

    url = BASE_URL.format(lat=LAT, lon=LON)

    response = requests.get(
        url,
        params={"token": TOKEN},
        timeout=20
    )

    response.raise_for_status()
    result = response.json()

    if result.get("status") != "ok":
        raise ValueError(
            f"AQICN API error: {result.get('data')}"
        )

    data = result["data"]
    iaqi = data.get("iaqi", {})

    air_quality = {
        "station": data.get("city", {}).get("name"),
        "aqi": data.get("aqi"),
        "pm25": iaqi.get("pm25", {}).get("v"),
        "pm10": iaqi.get("pm10", {}).get("v"),
        "no2": iaqi.get("no2", {}).get("v"),
        "so2": iaqi.get("so2", {}).get("v"),
        "co": iaqi.get("co", {}).get("v"),
        "o3": iaqi.get("o3", {}).get("v"),
        "timestamp": data.get("time", {}).get("iso")
    }

    return air_quality


if __name__ == "__main__":
    try:
        result = fetch_air_quality()

        print("\n--- Sukkur Air Quality ---")

        for key, value in result.items():
            print(f"{key}: {value}")

    except requests.exceptions.RequestException as error:
        print("API request failed:", error)

    except (ValueError, KeyError) as error:
        print("Configuration or response error:", error)
