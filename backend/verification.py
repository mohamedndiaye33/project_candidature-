from datetime import datetime

def calcul_age(date_naissance):
    today = datetime.today()
    naissance = datetime.strptime(date_naissance, "%Y-%m-%d")
    age = today.year - naissance.year
    # Ajuster si l'anniversaire n'est pas encore passé cette année
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