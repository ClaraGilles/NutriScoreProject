import logging
from ETL.api_fetcher import fetch_openfoodfacts_products
from ETL.transformer import clean_and_add_nutriscore_plus
from ETL.load import load_products_into_duckdb

# Config de logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

def run_pipeline():
    try:
        logging.info("🚀 Démarrage du pipeline Nutriscore")
        
        # Extraction
        df = fetch_openfoodfacts_products()
        logging.info(f"{len(df)} produits récupérés depuis OpenFoodFacts")
        
        # Transformation
        df_clean = clean_and_add_nutriscore_plus(df)
        logging.info("Transformation terminée (Nutriscore+)")

        # Chargement
        load_products_into_duckdb(df_clean)
        logging.info("✅ Pipeline terminé avec succès")
        
    except Exception as e:
        logging.error(f"❌ Erreur lors du pipeline : {e}", exc_info=True)

if __name__ == "__main__":
    run_pipeline()
