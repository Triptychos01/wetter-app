import httpx
import sys
import argparse
from datetime import datetime


def get_coordinates(city_name: str):
    """Holt die Koordinaten (Breiten- und Längengrad) für einen Ortsnamen."""
    url = f"https://geocoding-api.open-meteo.com/v1/search?name={city_name}&count=1&language=de&format=json"

    try:
        response = httpx.get(url, timeout=10.0)
        response.raise_for_status()
        data = response.json()

        if "results" in data and len(data["results"]) > 0:
            result = data["results"][0]
            return {
                "name": result.get("name"),
                "lat": result.get("latitude"),
                "lon": result.get("longitude"),
                "country": result.get("country"),
            }
        else:
            return None
    except Exception as e:
        return {"error": f"Fehler bei der Geocoding-Abfrage: {e}"}


def get_weather_data(lat: float, lon: float):
    """Ruft die Wetterdaten für die gegebenen Koordinaten ab."""
    url = (
        f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}"
        "&current=temperature_2m,relative_humidity_2m,wind_speed_10m"
        "&hourly=temperature_2m"
        "&daily=temperature_2m_max,temperature_2m_min,weather_code"
        "&timezone=auto"
        "&forecast_days=7"
    )

    try:
        response = httpx.get(url, timeout=10.0)
        response.raise_for_status()
        data = response.json()

        current = data["current"]
        daily = data["daily"]
        hourly = data["hourly"]

        # Aktuelle Stunde finden und nächste 24 Stunden extrahieren
        current_time = datetime.fromisoformat(current["time"])
        hourly_times = [datetime.fromisoformat(t) for t in hourly["time"]]
        start_idx = next(
            (i for i, t in enumerate(hourly_times) if t >= current_time), 0
        )
        hourly_24 = {
            "time": [t.strftime("%H:%M") for t in hourly_times[start_idx:start_idx + 24]],
            "temp": hourly["temperature_2m"][start_idx:start_idx + 24],
        }

        return {
            "temp": current["temperature_2m"],
            "humidity": current["relative_humidity_2m"],
            "windspeed": current["wind_speed_10m"],
            "temp_max": daily["temperature_2m_max"][0],
            "temp_min": daily["temperature_2m_min"][0],
            "weather_code": daily["weather_code"][0],
            "hourly_24": hourly_24,
            "daily": {
                "time": daily["time"],
                "temp_max": daily["temperature_2m_max"],
                "temp_min": daily["temperature_2m_min"],
                "weather_code": daily["weather_code"],
            },
        }
    except Exception as e:
        return {"error": str(e)}


def get_air_quality(lat: float, lon: float):
    """Ruft den aktuellen europäischen Luftqualitätsindex (AQI) ab."""
    url = (
        f"https://air-quality-api.open-meteo.com/v1/air-quality?latitude={lat}&longitude={lon}"
        "&current=european_aqi"
    )
    try:
        response = httpx.get(url, timeout=10.0)
        response.raise_for_status()
        data = response.json()
        return data["current"]["european_aqi"]
    except Exception:
        return None


def main():
    parser = argparse.ArgumentParser(
        description="Wetter-App: Aktuelle Wetterdaten und Vorhersage abrufen."
    )
    parser.add_argument(
        "city",
        nargs="?",
        default="Geesthacht",
        help="Name der Stadt (Standard: Geesthacht)",
    )

    args = parser.parse_args()

    location = get_coordinates(args.city)

    if location and "error" not in location:
        data = get_weather_data(location["lat"], location["lon"])
        if "error" not in data:
            display_name = f"{location['name']} ({location['country']})"
            print(f"--- Wetter in {display_name} ---")
            print(f"Aktuell: {data['temp']}°C")
            print(f"Luftfeuchtigkeit: {data['humidity']}%")
            print(f"Windgeschwindigkeit: {data['windspeed']} km/h")
            print(
                f"Vorhersage heute: Max {data['temp_max']}°C, Min {data['temp_min']}°C"
            )
        else:
            print(
                f"Fehler beim Abrufen der Wetterdaten: {data['error']}", file=sys.stderr
            )
    else:
        error_msg = (
            location["error"]
            if location and "error" in location
            else f"Konnte keine Koordinaten für '{args.city}' finden."
        )
        print(error_msg, file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
