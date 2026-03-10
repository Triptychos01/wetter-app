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

- **`weather.py`** — Kernlogik. Enthält `get_coordinates()` (Geocoding via Open-Meteo), `get_weather_data()` (Wetter + 7-Tage-Vorhersage via Open-Meteo) sowie eine `main()`-Funktion für den CLI-Betrieb mit `argparse`.
- **`app.py`** — Streamlit-Frontend. Importiert die beiden Funktionen aus `weather.py` und stellt sie als interaktive Web-Oberfläche dar (Stadteingabe, Metriken, Vorhersage-Tabelle, Karte).

Alle Wetterdaten kommen von der kostenlosen [Open-Meteo API](https://open-meteo.com/) — kein API-Key erforderlich. HTTP-Requests laufen über `httpx`.

`main.py` ist ein uv-generierter Platzhalter und gehört nicht zur App-Logik.
