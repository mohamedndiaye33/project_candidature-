import pandas as pd
from datetime import datetime

def calcul_age(date_naissance):
    today = datetime.today()
    naissance = datetime.strptime(date_naissance, "%Y-%m-%d")
    age = today.year - naissance.year
    if (today.month, today.day) < (naissance.month, naissance.day):
        age -= 1
    return age

def verifier_candidature(date_naissance, nationalite, nb_parrains, total_electeurs):
    age = calcul_age(date_naissance)
    pourcentage = (nb_parrains / total_electeurs) * 100

    if age <= 35:
        return "Rejet : âge insuffisant"
    if nationalite.lower() != "senegalaise":
        return "Rejet : nationalité invalide"
    if pourcentage < 0.8 or pourcentage > 1:
        return "Rejet : parrainage invalide"
    return "Candidature ACCEPTÉE"

def nettoyer_colonnes(df):
    """Nettoie les noms de colonnes pour éviter les erreurs : espaces, majuscules, accents"""
    df.columns = (
        df.columns
        .str.strip()        # supprime espaces en début/fin
        .str.lower()        # met en minuscules
        .str.replace(' ', '_')  # remplace espaces par _
        .str.replace("'", "")   # supprime apostrophes
    )
    return df

def compter_parrains_valides(df_parrains, df_electeurs):
    df_electeurs = nettoyer_colonnes(df_electeurs)
    df_parrains = nettoyer_colonnes(df_parrains)

    ids_electeurs = df_electeurs["numero_identification_nationale"]
    parrains_valides = df_parrains[
        df_parrains["numero_identification_nationale"].isin(ids_electeurs)
    ]
    return len(parrains_valides)

def main():
    # Lire les fichiers Excel
    df_electeurs = pd.read_excel("electeurs.xlsx", engine="openpyxl")
    df_parrains = pd.read_excel("parrains.xlsx", engine="openpyxl")

    total_electeurs = len(df_electeurs)
    nb_parrains = compter_parrains_valides(df_parrains, df_electeurs)

    # Exemple : données du candidat
    date_naissance_candidat = "1980-05-10"
    nationalite_candidat = "senegalaise"

    resultat = verifier_candidature(
        date_naissance_candidat,
        nationalite_candidat,
        nb_parrains,
        total_electeurs
    )

    print(f"Total électeurs : {total_electeurs}")
    print(f"Parrains valides : {nb_parrains}")
    print(f"Résultat de la candidature : {resultat}")

if __name__ == "__main__":
    main()