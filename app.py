import streamlit as st
from weather import get_coordinates, get_weather_data
from datetime import datetime
import locale

# Konfiguration der Seite
st.set_page_config(page_title="Wetter-App", page_icon="🌦️")

st.title("🌦️ Wetter-App")
st.write("Gib eine Stadt ein, um das aktuelle Wetter und die Vorhersage zu sehen.")

# Benutzereingabe
city_input = st.text_input("Stadt eingeben:", value="Geesthacht")
refresh = st.button("Aktualisieren")

if city_input:
    if refresh:
        st.cache_data.clear()
    with st.spinner(f"Suche Wetterdaten für {city_input}..."):
        location = get_coordinates(city_input)

        if location and "error" not in location:
            data = get_weather_data(location["lat"], location["lon"])

            if "error" not in data:
                st.subheader(f"Wetter in {location['name']} ({location['country']})")

                # Layout mit Spalten für aktuelle Daten
                col1, col2, col3 = st.columns(3)
                col1.metric("Temperatur", f"{data['temp']} °C")
                col2.metric("Luftfeuchtigkeit", f"{data['humidity']} %")
                col3.metric("Wind", f"{data['windspeed']} km/h")

                # Vorhersage-Bereich
                st.subheader("📅 7-Tage Vorhersage")

                locale.setlocale(locale.LC_TIME, "de_DE.UTF-8")

                forecast_data = []
                for i in range(len(data["daily"]["time"])):
                    date = datetime.strptime(data["daily"]["time"][i], "%Y-%m-%d")
                    forecast_data.append(
                        {
                            "Datum": date.strftime("%a, %d.%m"),
                            "🔼 Max": f"{data['daily']['temp_max'][i]} °C",
                            "🔽 Min": f"{data['daily']['temp_min'][i]} °C",
                        }
                    )

                st.table(forecast_data)

                # Karte anzeigen
                st.map(data={"lat": [location["lat"]], "lon": [location["lon"]]})
            else:
                st.error(f"Fehler beim Abrufen der Wetterdaten: {data['error']}")
        else:
            if location and "error" in location:
                st.error(location["error"])
            else:
                st.error(
                    f"Konnte keine Koordinaten für '{city_input}' finden. Bitte überprüfe die Schreibweise."
                )

# Footer
st.markdown("---")
st.caption("Daten bereitgestellt von [Open-Meteo.com](https://open-meteo.com/)")
