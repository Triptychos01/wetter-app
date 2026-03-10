# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Abhängigkeiten installieren
uv sync

# CLI-Version ausführen (Standard: Geesthacht)
uv run weather.py
uv run weather.py Hamburg

# Web-App starten (Streamlit läuft auf http://localhost:8501)
uv run python -m streamlit run app.py
```

> Hinweis: `uv run streamlit run app.py` schlägt fehl, da uv den `streamlit`-Einstiegspunkt nicht direkt auflöst. Stattdessen `python -m streamlit` verwenden.

## Architektur

Das Projekt hat zwei Nutzungsebenen über denselben Backend-Code:

- **`weather.py`** — Kernlogik mit drei Funktionen:
  - `get_coordinates(city_name)` — Geocoding via Open-Meteo
  - `get_weather_data(lat, lon)` — Aktuelles Wetter, stündliche Temperaturen (nächste 24h) und 7-Tage-Vorhersage via Open-Meteo
  - `get_air_quality(lat, lon)` — Europäischer Luftqualitätsindex (LQI) via Open-Meteo Air Quality API
  - `main()` — CLI-Betrieb mit `argparse`

- **`app.py`** — Streamlit-Frontend mit: Stadteingabe, Aktualisieren-Button (`st.cache_data.clear()`), 4 Metriken (Temperatur, Luftfeuchtigkeit, Wind, LQI mit Kategorie-Label), 24h-Temperaturliniendiagramm (`st.line_chart`), 7-Tage-Vorhersage-Tabelle (`st.dataframe`, ohne Index), Karte via `st.pydeck_chart` mit CARTO Voyager-Stil.

Alle Daten kommen von der kostenlosen [Open-Meteo API](https://open-meteo.com/) — kein API-Key erforderlich. HTTP-Requests laufen über `httpx`.

### LQI-Kategorien

| Wert    | Kategorie                        |
|---------|----------------------------------|
| 0–50    | gut                              |
| 51–100  | mäßig                            |
| 101–150 | ungesund für sensible Gruppen    |
| 151–200 | ungesund                         |

### Bekannte Einschränkung: Streamlit Cloud

Open-Meteo drosselt Anfragen von Streamlit-Cloud-IPs (429-Fehler), da alle dort gehosteten Apps dieselben IP-Adressen teilen. Die App funktioniert lokal einwandfrei. Für einen Cloud-Deploy wäre ein Wechsel zu einem Anbieter mit individuellen API-Keys (z. B. OpenWeatherMap) nötig.

`main.py` ist ein uv-generierter Platzhalter und gehört nicht zur App-Logik.
