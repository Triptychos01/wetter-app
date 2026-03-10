import streamlit as st
from weather import get_coordinates, get_weather_data, get_air_quality
from datetime import datetime
import locale
import pandas as pd
import pydeck as pdk

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
            aqi = get_air_quality(location["lat"], location["lon"])

            if "error" not in data:
                st.subheader(f"Wetter in {location['name']} ({location['country']})")

                # Layout mit Spalten für aktuelle Daten
                col1, col2, col3, col4 = st.columns(4)
                col1.metric("Temperatur", f"{data['temp']} °C")
                col2.metric("Luftfeuchtigkeit", f"{data['humidity']} %")
                col3.metric("Wind", f"{data['windspeed']} km/h")
                if aqi is not None:
                    if aqi <= 50:
                        aqi_label = "gut"
                    elif aqi <= 100:
                        aqi_label = "mäßig"
                    elif aqi <= 150:
                        aqi_label = "ungesund für sensible Gruppen"
                    else:
                        aqi_label = "ungesund"
                    col4.metric("Luftqualität (LQI)", aqi, aqi_label, delta_color="off")
                else:
                    col4.metric("Luftqualität (LQI)", "–")

                # Temperaturverlauf 24h
                st.subheader("🌡️ Temperaturverlauf – nächste 24 Stunden")
                hourly_df = pd.DataFrame(
                    {"Temperatur (°C)": data["hourly_24"]["temp"]},
                    index=data["hourly_24"]["time"],
                )
                st.line_chart(hourly_df)

                # Vorhersage-Bereich
                st.subheader("📅 7-Tage Vorhersage")

                locale.setlocale(locale.LC_TIME, "de_DE.UTF-8")

                forecast_data = []
                for i in range(len(data["daily"]["time"])):
                    date = datetime.strptime(data["daily"]["time"][i], "%Y-%m-%d")
                    forecast_data.append(
                        {
                            "Datum": date.strftime("%a %d.%m"),
                            "🔽 Min": f"{data['daily']['temp_min'][i]} °C",
                            "🔼 Max": f"{data['daily']['temp_max'][i]} °C",
                        }
                    )

                st.dataframe(pd.DataFrame(forecast_data), hide_index=True)

                # Karte anzeigen (helles Farbschema)
                st.pydeck_chart(pdk.Deck(
                    map_style="mapbox://styles/mapbox/light-v10",
                    initial_view_state=pdk.ViewState(
                        latitude=location["lat"],
                        longitude=location["lon"],
                        zoom=10,
                    ),
                    layers=[
                        pdk.Layer(
                            "ScatterplotLayer",
                            data=[{"lat": location["lat"], "lon": location["lon"]}],
                            get_position="[lon, lat]",
                            get_radius=500,
                            get_fill_color=[30, 136, 229],
                        )
                    ],
                ))
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
