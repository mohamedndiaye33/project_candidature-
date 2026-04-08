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

    pourcentage = (nb_parrains / total_electeurs) * 100 if total_electeurs > 0 else 0

    if age < 35:
        return False, "Âge insuffisant"

    if nationalite.lower() not in ["senegalaise", "sénégalaise"]:
        return False, "Nationalité invalide"

    if pourcentage < 0.8:
        return False, "Parrainage insuffisant"

    return True, "Candidature ACCEPTÉE"