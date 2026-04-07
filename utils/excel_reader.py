import pandas as pd

def lire_fichier_electoral(fichier):
    df = pd.read_excel(fichier)
    return df

def lire_parrainages(fichier):
    df = pd.read_excel(fichier)
    return df

def compter_parrains_valides(df_parrains, df_electeurs):
    # vérifier que les parrains existent dans le fichier électoral
    ids_electeurs = df_electeurs["numero_identification_nationale"]

    parrains_valides = df_parrains[
        df_parrains["numero_identification_nationale"].isin(ids_electeurs)
    ]

    return len(parrains_valides)