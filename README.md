# Wetter-App (Geesthacht)

Ein einfaches Python-Skript, um das aktuelle Wetter für Geesthacht abzurufen. Nutzt die kostenlose [Open-Meteo API](https://open-meteo.com/).

## Voraussetzungen

- [Python](https://www.python.org/) (Version >= 3.12 empfohlen)
- [uv](https://github.com/astral-sh/uv) (Moderner Python Paket-Manager)

## Installation

1. Repository klonen:
   ```bash
   git clone https://github.com/Triptychos01/wetter-app.git
   cd wetter-app/Wetter-App
   ```

2. Abhängigkeiten installieren:
   ```bash
   uv sync
   ```

## Nutzung

### CLI-Version
Führe das Skript mit `uv` aus. Du kannst optional einen Städtenamen angeben:

```bash
# Standard: Geesthacht
uv run weather.py

# Beliebiger Ort:
uv run weather.py Hamburg
```

### Web-App (Interaktive Oberfläche)
Du kannst die Wetter-App auch mit einer grafischen Oberfläche im Browser starten:

```bash
uv run streamlit run app.py
```

## Zukünftige Funktionen

- [x] Unterstützung für verschiedene Städte über Kommandozeilenparameter.
- [x] Anzeige von Luftfeuchtigkeit und Wettervorhersage.
- [x] Integration einer interaktiven Benutzeroberfläche (Streamlit).
