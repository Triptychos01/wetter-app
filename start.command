#!/bin/zsh
cd "$(dirname "$0")"
uv run python -m streamlit run app.py
