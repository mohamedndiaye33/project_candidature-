import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from datetime import datetime
import matplotlib.pyplot as plt

from backend.gestion_db import ajouter_candidat, lire_candidats
from utils.lecture_csv import lire_parrains, compter_electeurs
from utils.logique_verification import (
    verifier_eligibilite_candidat,
    verifier_validite_parrains,
    calculer_statistiques
)


class AppCandidature:
    def __init__(self, root):
        self.root = root
        self.root.title("Cour Suprême du Sénégal")
        self.root.geometry("1100x750")
        self.root.configure(bg="#0f172a")

        self.fichier_parrainage = None

        self._header()
        self._formulaire()
        self._boutons()
        self._resultat()
        self._dashboard()
        self._tableau()

    # 🏛 HEADER
    def _header(self):
        frame = tk.Frame(self.root, bg="#020617", pady=15)
        frame.pack(fill="x")

        tk.Label(frame,
                 text="🏛️ COUR SUPRÊME DU SÉNÉGAL",
                 font=("Arial", 20, "bold"),
                 bg="#020617",
                 fg="#facc15").pack()

        tk.Label(frame,
                 text="Système d'Arbitrage des Candidatures Présidentielles",
                 font=("Arial", 11),
                 bg="#020617",
                 fg="#94a3b8").pack()

    # 📋 FORMULAIRE CENTRÉ
    def _formulaire(self):
        container = tk.Frame(self.root, bg="#0f172a")
        container.pack(expand=True)

        frame = tk.LabelFrame(container,
                              text="📋 Informations du Candidat",
                              bg="#1e293b",
                              fg="white",
                              font=("Arial", 12, "bold"),
                              padx=25, pady=20)
        frame.pack()

        self.entries = {}

        gauche = [
            ("Nom", "nom"),
            ("Date (JJ/MM/AAAA)", "date_naissance"),
            ("Nationalité", "nationalite")
        ]

        droite = [
            ("Prénom", "prenom"),
            ("Lieu de naissance", "lieu_naissance"),
            ("NIN", "nin")
        ]

        for i, (label, key) in enumerate(gauche):
            tk.Label(frame, text=label, bg="#1e293b", fg="white").grid(row=i, column=0, padx=15, pady=10, sticky="e")
            e = tk.Entry(frame, width=30, bg="#e2e8f0")
            e.grid(row=i, column=1, padx=10)
            self.entries[key] = e

        for i, (label, key) in enumerate(droite):
            tk.Label(frame, text=label, bg="#1e293b", fg="white").grid(row=i, column=2, padx=25, pady=10, sticky="e")
            e = tk.Entry(frame, width=30, bg="#e2e8f0")
            e.grid(row=i, column=3, padx=10)
            self.entries[key] = e

        tk.Button(frame,
                  text="📂 Importer fichier (optionnel)",
                  bg="#f59e0b",
                  fg="white",
                  width=25,
                  command=self._importer).grid(row=3, column=1, columnspan=2, pady=20)

    # 🔘 BOUTONS
    def _boutons(self):
        frame = tk.Frame(self.root, bg="#0f172a")
        frame.pack(pady=10)

        tk.Button(frame, text="✅ Vérifier", bg="#22c55e", fg="white", width=22,
                  command=self._verifier).grid(row=0, column=0, padx=10)

        tk.Button(frame, text="🗑 Effacer", bg="#ef4444", fg="white", width=18,
                  command=self._reset).grid(row=0, column=1, padx=10)

        tk.Button(frame, text="📊 Graphique", bg="#8b5cf6", fg="white", width=18,
                  command=self._graphique).grid(row=0, column=2, padx=10)

    # 📊 RESULTAT
    def _resultat(self):
        self.label = tk.Label(self.root,
                              text="En attente de vérification...",
                              font=("Arial", 13, "bold"),
                              bg="#1e293b",
                              fg="white",
                              pady=10)
        self.label.pack(fill="x", padx=20, pady=10)

    # 📊 DASHBOARD
    def _dashboard(self):
        frame = tk.LabelFrame(self.root,
                              text="📊 Tableau de Bord",
                              bg="#1e293b",
                              fg="white",
                              font=("Arial", 11, "bold"))
        frame.pack(fill="x", padx=20, pady=10)

        self.stat_parrains = tk.Label(frame, text="Parrains\n0",
                                     bg="#3b82f6", fg="white",
                                     font=("Arial", 11, "bold"),
                                     width=20, height=3)
        self.stat_parrains.grid(row=0, column=0, padx=15, pady=10)

        self.stat_pourcentage = tk.Label(frame, text="0%",
                                         bg="#22c55e", fg="white",
                                         font=("Arial", 11, "bold"),
                                         width=20, height=3)
        self.stat_pourcentage.grid(row=0, column=1, padx=15)

        self.stat_verdict = tk.Label(frame, text="---",
                                     bg="#ef4444", fg="white",
                                     font=("Arial", 11, "bold"),
                                     width=20, height=3)
        self.stat_verdict.grid(row=0, column=2, padx=15)

    # 📋 TABLEAU
    def _tableau(self):
        colonnes = ("ID", "Prenom", "Nom", "Naissance", "Lieu", "Nationalite", "NIN", "Statut")

        self.table = ttk.Treeview(self.root, columns=colonnes, show="headings")

        for col in colonnes:
            self.table.heading(col, text=col)
            self.table.column(col, width=120, anchor="center")

        self.table.pack(fill="both", expand=True, padx=20, pady=10)

    # 📂 IMPORT (optionnel)
    def _importer(self):
        self.fichier_parrainage = filedialog.askopenfilename()

    # 🔥 VERIFICATION
    def _verifier(self):
        data = {k: v.get().strip() for k, v in self.entries.items()}

        try:
            date_obj = datetime.strptime(data["date_naissance"], "%d/%m/%Y")
            age = datetime.today().year - date_obj.year
        except:
            messagebox.showerror("Erreur", "Date invalide")
            return

        ok, _ = verifier_eligibilite_candidat(age, data["nationalite"])

        nb_valides = 0
        pourcentage = 0
        verdict = "NON CALCULÉ"

        if self.fichier_parrainage:
            parrains = lire_parrains(self.fichier_parrainage)
            nb_valides, _ = verifier_validite_parrains(parrains)

            total = compter_electeurs("electeurs.csv")
            pourcentage, verdict = calculer_statistiques(nb_valides, total)

        # Dashboard
        self.stat_parrains.config(text=f"Parrains\n{nb_valides}")
        self.stat_pourcentage.config(text=f"{pourcentage}%")
        self.stat_verdict.config(text=verdict)

        if ok and "ADMISSIBLE" in verdict:
            statut = "ACCEPTEE"
            self.label.config(text=f"✅ ACCEPTÉE ({pourcentage}%)", fg="#22c55e")
        else:
            statut = "REJETEE"
            self.label.config(text=f"❌ REJETÉE ({pourcentage}%)", fg="#ef4444")

        ajouter_candidat(
            data["prenom"],
            data["nom"],
            date_obj.strftime("%Y-%m-%d"),
            data["lieu_naissance"],
            data["nationalite"],
            data["nin"],
            statut
        )

        self._afficher_db()

    # 📊 AFFICHER DB
    def _afficher_db(self):
        for row in self.table.get_children():
            self.table.delete(row)

        for c in lire_candidats():
            self.table.insert("", "end", values=c)

    # 📈 GRAPHIQUE
    def _graphique(self):
        candidats = lire_candidats()

        acceptes = sum(1 for c in candidats if c[-1] == "ACCEPTEE")
        rejetes = sum(1 for c in candidats if c[-1] == "REJETEE")

        labels = ["Acceptés", "Rejetés"]
        valeurs = [acceptes, rejetes]

        plt.figure()

        bars = plt.bar(labels, valeurs)

        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2, height,
                     f'{int(height)}',
                     ha='center', va='bottom')

        plt.title("📊 Statistiques des candidatures")
        plt.ylabel("Nombre")
        plt.grid(axis='y', linestyle='--', alpha=0.5)

        plt.show()

    # 🔄 RESET
    def _reset(self):
        for entry in self.entries.values():
            entry.delete(0, tk.END)
        self.label.config(text="En attente de vérification...")


# 🚀 LANCEMENT
if __name__ == "__main__":
    root = tk.Tk()
    app = AppCandidature(root)
    root.mainloop()