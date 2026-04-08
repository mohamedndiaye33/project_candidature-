

def verifier_eligibilite_candidat(age, nationalite):
    """Vérifie si le candidat a plus de 35 ans et est Sénégalais."""
    erreurs = []
    
    # 1. Vérification de l'âge
    if age < 35:
        erreurs.append(f"Âge insuffisant : {age} ans (Minimum 35 ans)")
    
    # 2. Vérification de la nationalité
    if nationalite.lower() != "sénégalaise":
        erreurs.append("Nationalité non conforme (doit être exclusivement Sénégalaise)")
    
    est_valide = len(erreurs) == 0
    return est_valide, erreurs

def verifier_validite_parrains(liste_parrains):
    """
    Vérifie la validité des parrains et détecte les doublons.
    Prend une liste de dictionnaires [{'cni': '...', 'nom': '...'}, ...]
    """
    parrains_uniques = set()
    doublons = 0
    
    for parrain in liste_parrains:
        cni = parrain.get('cni')
        if cni in parrains_uniques:
            doublons += 1
        else:
            parrains_uniques.add(cni)
            
    valides = len(parrains_uniques)
    return valides, doublons

def calculer_statistiques(nb_parrains_valides, total_fichier_electoral):
    """Calcule le pourcentage de parrainage et donne le verdict."""
    if total_fichier_electoral == 0:
        return 0, "Erreur : Fichier électoral vide"
        
    pourcentage = (nb_parrains_valides / total_fichier_electoral) * 100
    
    # Seuil légal : 0.8%
    if pourcentage >= 0.8:
        verdict = "ADMISSIBLE"
    else:
        verdict = "REJETÉ (Seuil de 0.8% non atteint)"
        
    return round(pourcentage, 2), verdict