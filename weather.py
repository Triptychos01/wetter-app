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
                "country": result.get("country")
            }
        else:
            return None
    except Exception as e:
        print(f"Fehler bei der Geocoding-Abfrage: {e}", file=sys.stderr)
        return None

def get_weather(lat: float, lon: float, city_display_name: str):
    """Ruft die Wetterdaten für die gegebenen Koordinaten ab."""
    # Wir fragen aktuelle Daten (Temp, Feuchtigkeit, Wind) und die Vorhersage für heute ab
    url = (
        f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}"
        "&current=temperature_2m,relative_humidity_2m,wind_speed_10m"
        "&daily=temperature_2m_max,temperature_2m_min,weather_code"
        "&timezone=auto"
    )
    
    try:
        response = httpx.get(url, timeout=10.0)
        response.raise_for_status()
        data = response.json()
        
        # Aktuelles Wetter
        current = data["current"]
        temp = current["temperature_2m"]
        humidity = current["relative_humidity_2m"]
        windspeed = current["wind_speed_10m"]
        
        # Vorhersage für heute (Index 0)
        daily = data["daily"]
        temp_max = daily["temperature_2m_max"][0]
        temp_min = daily["temperature_2m_min"][0]
        
        print(f"--- Wetter in {city_display_name} ---")
        print(f"Aktuell: {temp}°C")
        print(f"Luftfeuchtigkeit: {humidity}%")
        print(f"Windgeschwindigkeit: {windspeed} km/h")
        print(f"Vorhersage heute: Max {temp_max}°C, Min {temp_min}°C")
        
    except httpx.HTTPStatusError as e:
        print(f"Fehler beim Abrufen der Wetterdaten von Open-Meteo: {e}", file=sys.stderr)
    except Exception as e:
        print(f"Ein unerwarteter Fehler ist aufgetreten: {e}", file=sys.stderr)

def main():
    parser = argparse.ArgumentParser(description="Wetter-App: Aktuelle Wetterdaten und Vorhersage abrufen.")
    parser.add_argument("city", nargs="?", default="Geesthacht", help="Name der Stadt (Standard: Geesthacht)")
    
    args = parser.parse_args()
    
    location = get_coordinates(args.city)
    
    if location:
        display_name = f"{location['name']} ({location['country']})"
        get_weather(location['lat'], location['lon'], display_name)
    else:
        print(f"Konnte keine Koordinaten für '{args.city}' finden.", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
