FROM python:3.11-slim

# Installer dépendances système minimales
RUN apt-get update && apt-get install -y \
    curl build-essential \
    && rm -rf /var/lib/apt/lists/*

# Répertoire de travail
WORKDIR /app

# Copier requirements et installer les dépendances Python
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

RUN python -m spacy download fr_core_news_sm

# Copier le code du projet
COPY . .

# S'assurer que /app/src est dans le PYTHONPATH (pour les imports ETL)
ENV PYTHONPATH=/app/src

# Rendre le script d'entrée exécutable
RUN chmod +x entrypoint.sh

# Expose Streamlit
EXPOSE 8501

# Lancer le script d'entrée
ENTRYPOINT ["./entrypoint.sh"]
