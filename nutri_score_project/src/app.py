import streamlit as st
import duckdb
import pandas as pd

# Titre de l'application
st.title("Recherche produit NutriScore")

# Connexion à la DB DuckDB
con = duckdb.connect('data/processed/products_data.db')

# Charger la table entière
df = con.execute("SELECT * FROM products_data").fetchdf()

# Affichage de toute la table
st.subheader("Table complète des produits")
st.dataframe(df)

# Champ de texte pour la recherche
query = st.text_input("Tapez le nom du produit :")

if query:
    # Filtrer les lignes contenant le mot dans product_name (insensible à la casse)
    result = df[df['product_name'].str.contains(query, case=False, na=False)]
    
    if not result.empty:
        st.subheader(f"Résultats pour : {query}")
        st.dataframe(result)
    else:
        st.warning("Aucun produit trouvé pour cette recherche.")
