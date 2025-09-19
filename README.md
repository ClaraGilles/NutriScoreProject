# NutriScore Project

Ce projet permet de récupérer des données de produits alimentaires (catégorie salty snacks) depuis OpenFoodFacts, de les nettoyer et d’ajouter un **score NutriScore+** basé sur les ingrédients, le groupe NOVA et les labels. Il propose également une interface Streamlit pour rechercher et visualiser les produits.

---

## Structure du projet



```bash
.
│── nutri_score_project/       # Dossier principal contenant le code et les données
│   │
│   ├── data/                  # Dossier pour stocker les fichiers
│   │   ├── raw/               # Données brutes récupérées depuis l'API OpenFoodFacts (Parquet)
│   │   └── processed/         # Données nettoyées et enrichies avec NutriScore+, stockées DuckDB
│   │
│   ├── src/                   # Code source principal
│   │   ├── ETL/               # Pipeline ETL
│   │   │   ├── api_fetcher.py     # Récupération des données depuis OpenFoodFacts
│   │   │   ├── transformer.py     # Nettoyage des données et ajout de la colonne NutriScore+
│   │   │   └── load.py            # Gestion de la base DuckDB : création de table, insertion sécurisée
│   │   │
│   │   ├── app.py             # Interface Streamlit pour recherche et visualisation des produits
│   │   ├── main.py            # Exécution automatique du pipeline ETL complet
│   │   └── Dockerfile         # Conteneurisation du projet
│   │
│   │── entrypoint.sh          # Script d’entrée Docker pour lancer le pipeline ETL et Streamlit
│   └── requirements.txt       # Dépendances Python (pandas, duckdb, spacy, streamlit, etc.)
│
│── docker-compose.yml         # Orchestration du conteneur avec volumes pour les données persistantes
│── .gitignore                 # Ignorer fichiers temporaires, .pyc, venv, data bruts si nécessaire
└── README.md                  # Documentation du projet : description, installation, utilisation
```

## Fonctionnalités

ETL complet : fetch → transform → load.

Nettoyage des données : conversion des listes en chaînes, gestion des NaN, calcul du NutriScore+.

Base DuckDB : insertion sécurisée et persistante des données transformées.

Interface Streamlit : recherche rapide et visualisation des produits.