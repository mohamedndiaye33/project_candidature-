import csv
from datetime import datetime

# Lire fichier électeurs
with open("electeurs.csv", newline='', encoding='latin-1') as f:
    lecteur = list(csv.reader(f, delimiter=';'))
    nb_electeurs = len(lecteur) - 1

# Lire fichier parrains
with open("parrains.csv", newline='', encoding='latin-1') as f:
    lecteur = list(csv.reader(f, delimiter=';'))
    nb_parrains = len(lecteur) - 1

# Calcul
pourcentage = (nb_parrains / nb_electeurs) * 100

def calcul_age(date_naissance):
    today = datetime.today()
    naissance = datetime.strptime(date_naissance, "%Y-%m-%d")
    age = today.year - naissance.year
    # Ajuster si l'anniversaire n'est pas encore passé cette année
    if (today.month, today.day) < (naissance.month, naissance.day):
        age -= 1
    return age

date_naissance = "1980-05-10"
nationalite = "senegalaise"

age = calcul_age(date_naissance)

print("Electeurs :", nb_electeurs)
print("Parrains :", nb_parrains)
print("Pourcentage :", pourcentage)
print("Age :", age)

if age >= 35 and nationalite.lower() == "senegalaise" and pourcentage >= 0.8:
    print("✅ ACCEPTÉE")
else:
    print("❌ REJETÉE")