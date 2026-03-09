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

Führe das Skript einfach mit `uv` aus. Du kannst optional einen Städtenamen angeben (Standard ist Geesthacht):

```bash
# Standard: Geesthacht
uv run weather.py

# Beliebiger Ort:
uv run weather.py Hamburg
uv run weather.py Berlin
```

Das Skript gibt die aktuelle Temperatur und Windgeschwindigkeit für den gewählten Ort aus.

## Zukünftige Funktionen

- [x] Unterstützung für verschiedene Städte über Kommandozeilenparameter.
- [ ] Anzeige von Luftfeuchtigkeit und Wettervorhersage.
- [ ] Integration einer interaktiven Benutzeroberfläche.
