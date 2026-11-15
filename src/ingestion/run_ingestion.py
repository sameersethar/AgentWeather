
import json
from datetime import datetime
from pathlib import Path

from weather_api import fetch_weather
from air_quality_api import fetch_air_quality


def run():
    print("Starting AgentWeather data ingestion...")

    weather = fetch_weather()
    air_quality = fetch_air_quality()

    combined_data = {
        "collected_at": datetime.now().astimezone().isoformat(),
        "location": "Sukkur, Pakistan",
        "weather": weather,
        "air_quality": air_quality
    }

    output_dir = Path("data/raw")
    output_dir.mkdir(parents=True, exist_ok=True)

    filename = datetime.now().strftime(
        "agentweather_%Y%m%d_%H%M%S.json"
    )

    output_file = output_dir / filename

    with output_file.open("w", encoding="utf-8") as file:
        json.dump(combined_data, file, indent=4)

    print("\nData ingestion completed!")
    print("Saved:", output_file)


if __name__ == "__main__":
    try:
        run()
    except Exception as error:
        print("Ingestion failed:", error)
