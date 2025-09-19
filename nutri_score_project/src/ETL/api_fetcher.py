import os
import requests
import pandas as pd
import streamlit as st

# Dossier où sauvegarder les données brutes
RAW_DATA_FOLDER = "data/raw"
os.makedirs(RAW_DATA_FOLDER, exist_ok=True)

fields = [
    "product_name",               # Nom du produit
    "code",                       # Code-barres (identifiant unique)
    "brands",                     # Marque
    "categories_tags",            # Catégorie (utile pour filtrer viande/lait)
    "nutriscore_grade",           # Nutri-Score (A-E)
    "nova_group",                 # Groupe NOVA (1 à 4)
    "ingredients_text",           # Liste brute des ingrédients
    "ingredients",                # Liste structurée
    "additives_tags",             # Additifs présents
    "labels_tags",                # Labels (bio, AB, etc.)
    "origins_tags",               # Origine des ingrédients
    "countries_tags",             # Pays de commercialisation
    "manufacturing_places_tags",  # Lieux de fabrication
    "packaging_tags",             # Emballage (recyclable ou non)
    "ecoscore_score",             # Score environnemental
    "ecoscore_grade",             # Grade (A-E) éco-score
    "environment_impact_level_tags",  # Impact environnemental
]

def fetch_openfoodfacts_products(category_tags="salty-snacks", page_size=200):
    url = "https://world.openfoodfacts.org/api/v2/search"
    params = {
        "categories_tags": category_tags,
        "fields": ",".join(fields),
        "page_size": page_size,
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()
    
    products = data.get("products", [])
    df = pd.DataFrame(products)
    print(df)

    # Chemin complet du fichier parquet
    output_path = os.path.join(RAW_DATA_FOLDER, "open_food_data.parquet")
    df.to_parquet(output_path, index=False)

    print(f"✅ { len(df)} produits sauvegardés dans {output_path}")
    return df
