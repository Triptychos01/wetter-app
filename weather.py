import httpx
import sys
import argparse

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
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
    
    try:
        response = httpx.get(url, timeout=10.0)
        response.raise_for_status()
        data = response.json()
        
        current = data["current_weather"]
        temp = current["temperature"]
        windspeed = current["windspeed"]
        
        print(f"Wetter in {city_display_name}: {temp}°C, Windgeschwindigkeit: {windspeed} km/h")
    except httpx.HTTPStatusError as e:
        print(f"Fehler beim Abrufen der Wetterdaten von Open-Meteo: {e}", file=sys.stderr)
    except Exception as e:
        print(f"Ein unerwarteter Fehler ist aufgetreten: {e}", file=sys.stderr)

def main():
    parser = argparse.ArgumentParser(description="Wetter-App: Aktuelle Wetterdaten für einen beliebigen Ort abrufen.")
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
