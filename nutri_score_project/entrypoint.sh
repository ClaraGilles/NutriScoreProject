#!/bin/bash
set -e

# 1️⃣ Lancer le pipeline ETL
python src/main.py

# 2️⃣ Lancer Streamlit
streamlit run src/app.py --server.port=8501 --server.address=0.0.0.0
