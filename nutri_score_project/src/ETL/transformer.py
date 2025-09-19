import pandas as pd
import spacy
from spacy.matcher import PhraseMatcher
import re

# Charger le modèle français
nlp = spacy.load("fr_core_news_sm")

# 🟢 Bons ingrédients
GOOD_INGREDIENTS = [
    "pomme de terre", "patate douce", "betterave", "carotte", "courge", "pois", "maïs", "pois chiche",
    "blé complet", "riz complet", "avoine", "quinoa", "orge", "épeautre", "millet",
    "amande", "noix", "noisette", "cacahuète", "pistache", "graines de tournesol",
    "graines de courge", "graines de lin", "graines de sésame",
    "lentille", "haricot", "pois cassé", "paprika", "curcuma", "cumin", "piment", "ail", "oignon",
    "herbes de Provence", "thym", "romarin",
    "sel marin", "sel de mer", "huile d'olive", "huile de colza", "huile de tournesol non raffinée"
]

# 🔴 Mauvais ingrédients
BAD_INGREDIENTS = [
    "sucre", "glucose", "fructose", "saccharose", "maltose", "maltodextrine",
    "sirop de glucose", "sirop de maïs", "sirop de fructose", "sirop inverti",
    "sirop d'agave", "huile de palme", "huile de coco raffinée", "huile de soja raffinée",
    "huile végétale partiellement hydrogénée", "margarine industrielle",
    "graisse végétale hydrogénée", "farine raffinée", "farine blanche",
    "produit instantané", "arômes artificiels", "arôme artificiel", "arôme synthétique",
    "exhausteur de goût", "stabilisant chimique", "émulsifiant industriel",
    "agent de conservation", "gomme xanthane synthétique", "colorant artificiel",
    "concentré de jus industriel", "produit enrichi artificiellement", "poudre aromatisée",
    "boisson instantanée sucrée", "protéines végétales texturées", "sirop de riz",
    "huile partiellement hydrogénée"
]

# Regex pour E-numbers
E_NUMBER_PATTERN = re.compile(r"\bE\d{2,3}\b", re.IGNORECASE)

# PhraseMatchers
matcher_good = PhraseMatcher(nlp.vocab, attr="LOWER")
matcher_bad = PhraseMatcher(nlp.vocab, attr="LOWER")
matcher_good.add("GOOD", [nlp(text) for text in GOOD_INGREDIENTS])
matcher_bad.add("BAD", [nlp(text) for text in BAD_INGREDIENTS])

def score_ingredients_spacy(text: str) -> int:
    if not text or pd.isna(text):
        return 0
    doc = nlp(str(text).lower())
    score = len(matcher_good(doc)) - len(matcher_bad(doc)) - len(E_NUMBER_PATTERN.findall(str(text)))
    return score

def nutriscore_plus_spacy_row(row: pd.Series) -> int:
    score = 0
    # Ingrédients
    ingredients_text = row.get("ingredients_text", "")
    score += score_ingredients_spacy(ingredients_text)
    # NOVA
    nova = row.get("nova_group", 4)
    try:
        nova = int(nova)
    except (ValueError, TypeError):
        nova = 4
    score -= (nova - 1) * 2
    # Labels
    labels = row.get("labels_tags", [])
    if not isinstance(labels, list):
        labels = []
    if any("bio" in str(l).lower() for l in labels):
        score += 3
    if any("label-rouge" in str(l).lower() for l in labels):
        score += 2
    return score

def clean_and_add_nutriscore_plus(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    
    # Ajouter la colonne nutriscore_plus
    df['nutriscore_plus'] = df.apply(nutriscore_plus_spacy_row, axis=1)
    
    # Colonnes numériques
    int_cols = ['nova_group', 'ecoscore_score']
    for col in int_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)
    
    # Colonnes listes → convertir chaque élément en string puis joindre
    list_cols = [
        'ingredients', 'additives_tags', 'labels_tags', 
        'origins_tags', 'countries_tags', 'manufacturing_places_tags', 'packaging_tags'
    ]
    for col in list_cols:
        if col in df.columns:
            df[col] = df[col].apply(
                lambda x: ', '.join([str(i) for i in x]) if isinstance(x, list) 
                else (str(x) if pd.notna(x) else "")
            )
    
    # Colonnes objets restantes → remplacer NaN par chaîne vide
    object_cols = df.select_dtypes(include='object').columns.tolist()
    for col in object_cols:
        df[col] = df[col].fillna('')
    
    # Debug
    print("ceci est le df transfo :\n", df.head())
    print("\nles types :\n", df.dtypes)
    print("\ninfo :")
    df.info()
    
    return df
