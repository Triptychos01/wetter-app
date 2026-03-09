import httpx
import sys

def get_weather():
    # Geesthacht coordinates
    lat = 53.43
    lon = 10.37
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
    
    try:
        response = httpx.get(url, timeout=10.0)
        response.raise_for_status()
        data = response.json()
        current = data["current_weather"]
        temp = current["temperature"]
        windspeed = current["windspeed"]
        print(f"Wetter in Geesthacht: {temp}°C, Windgeschwindigkeit: {windspeed} km/h")
    except httpx.HTTPStatusError as e:
        print(f"Fehler beim Abrufen der Wetterdaten von Open-Meteo: {e}", file=sys.stderr)
    except Exception as e:
        print(f"Ein unerwarteter Fehler ist aufgetreten: {e}", file=sys.stderr)

if __name__ == "__main__":
    get_weather()
