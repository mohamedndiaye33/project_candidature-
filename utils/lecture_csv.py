import csv

def lire_parrains(fichier):
    parrains = []

    with open(fichier, encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter=';')

        for row in reader:
            parrains.append({
                "cni": row.get("NIN") or row.get("cni"),
                "nom": row.get("Nom", "")
            })

    return parrains


def compter_electeurs(fichier):
    with open(fichier, encoding="utf-8") as f:
        reader = csv.reader(f, delimiter=';')
        next(reader)
        return sum(1 for _ in reader)