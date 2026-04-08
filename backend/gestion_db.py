import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, 'cour_supreme.db')


def initialiser_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS candidats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            prenom TEXT NOT NULL,
            nom TEXT NOT NULL,
            date_naissance TEXT NOT NULL,
            lieu_naissance TEXT NOT NULL,
            nationalite TEXT NOT NULL,
            nin TEXT UNIQUE NOT NULL,
            statut TEXT
        )
    ''')

    conn.commit()
    conn.close()


def ajouter_candidat(prenom, nom, date_naiss, lieu_naiss, nationalite, nin, statut):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        cursor.execute('''
            INSERT INTO candidats (prenom, nom, date_naissance, lieu_naissance, nationalite, nin, statut)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (prenom, nom, date_naiss, lieu_naiss, nationalite, nin, statut))

        conn.commit()

    except sqlite3.IntegrityError:
        print("❌ NIN déjà existant")

    finally:
        conn.close()


def lire_candidats():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM candidats")
    data = cursor.fetchall()

    conn.close()
    return data