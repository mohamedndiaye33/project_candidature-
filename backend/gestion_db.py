import sqlite3
import os

# Définition du chemin de la base de données (à la racine du projet)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, 'cour_supreme.db')

def initialiser_db():
    """Crée la base de données et la table des candidats si elles n'existent pas."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Création de la table avec TOUTES les colonnes demandées dans le NB 3
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS candidats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            prenom TEXT NOT NULL,
            nom TEXT NOT NULL,
            date_naissance TEXT NOT NULL,
            lieu_naissance TEXT NOT NULL,
            nationalite TEXT NOT NULL,
            nin TEXT UNIQUE NOT NULL,
            fichier_parrainage TEXT NOT NULL,
            statut TEXT DEFAULT 'En attente'
        )
    ''')
    
    conn.commit()
    conn.close()
    print(f"Base de données initialisée avec succès : {DB_PATH}")

def ajouter_candidat(prenom, nom, date_naiss, lieu_naiss, nationalite, nin, fichier_parrainage):
    """Permet de stocker les informations d'un candidat dans la base."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO candidats (prenom, nom, date_naissance, lieu_naissance, nationalite, nin, fichier_parrainage)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (prenom, nom, date_naiss, lieu_naiss, nationalite, nin, fichier_parrainage))
        conn.commit()
        print(f"Candidat {prenom} {nom} enregistré avec succès !")
    except sqlite3.IntegrityError:
        print(f"Erreur : Le NIN {nin} existe déjà dans la base.")
    except Exception as e:
        print(f"Une erreur est survenue : {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    # Cette partie s'exécute quand tu lances le fichier directement
    initialiser_db()
    
    # Test (Optionnel) : Tu peux décommenter la ligne suivante pour tester un ajout
    # ajouter_candidat("Moussa", "Diop", "1985-05-12", "Dakar", "Sénégalaise", "123456789", "parrainage_moussa.xlsx")