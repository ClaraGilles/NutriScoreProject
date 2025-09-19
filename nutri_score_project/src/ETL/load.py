import duckdb as dd
import pandas as pd

def load_products_into_duckdb(df):
    """Charge les données produits dans DuckDB"""
    if df.empty:
        print("Aucune donnée à charger dans DuckDB.")
        return

    # Connexion à DuckDB (BD persistante)
    con = dd.connect('data/processed/products_data.db')

    # Création de la table si elle n'existe pas
    con.execute('''
    CREATE TABLE IF NOT EXISTS products_data (
        product_name VARCHAR,
        code VARCHAR,
        brands VARCHAR,
        categories_tags VARCHAR,
        nutriscore_grade VARCHAR,
        nova_group INTEGER,
        ingredients_text VARCHAR,
        ingredients VARCHAR,
        additives_tags VARCHAR,
        labels_tags VARCHAR,
        origins_tags VARCHAR,
        countries_tags VARCHAR,
        manufacturing_places_tags VARCHAR,
        packaging_tags VARCHAR,
        ecoscore_score INTEGER,
        ecoscore_grade VARCHAR,
        environment_impact_level_tags VARCHAR,
        nutriscore_plus INTEGER
    );
    ''')


    # Insertion des données
    con.executemany('''
    INSERT INTO products_data (
        product_name, code, brands, categories_tags,
        nutriscore_grade, nova_group, ingredients_text, ingredients,
        additives_tags, labels_tags, origins_tags, countries_tags,
        manufacturing_places_tags, packaging_tags,
        ecoscore_score, ecoscore_grade, environment_impact_level_tags,
        nutriscore_plus
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    ''', df.values.tolist())

    print(f"{len(df)} enregistrements chargés dans DuckDB.")

    # Optionnel : sauvegarde en Parquet pour analyse externe
    df.to_parquet('data/clean/products_data.parquet')

    con.close()
