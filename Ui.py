import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from datetime import datetime
import sys
import os

# Ajout du chemin pour importer les modules des camarades
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from backend.verification import verifier_candidat
    from utils.excel_reader import lire_fichier_excel
except ImportError:
    pass  # Les modules seront connectés plus tard


class AppCandidature:
    def __init__(self, root):
        self.root = root
        self.root.title("Cour Suprême du Sénégal - Recevabilité des Candidatures")
        self.root.geometry("900x700")
        self.root.configure(bg="#1a3a5c")
        self.root.resizable(True, True)

        self.fichier_parrainage = None
        self.resultats = []

        self._creer_header()
        self._creer_formulaire()
        self._creer_boutons()
        self._creer_zone_resultats()
        self._creer_dashboard()

    # ─────────────── HEADER ───────────────
    def _creer_header(self):
        header = tk.Frame(self.root, bg="#0d2438", pady=15)
        header.pack(fill="x")

        tk.Label(
            header,
            text="🏛️ COUR SUPRÊME DU SÉNÉGAL",
            font=("Arial", 18, "bold"),
            bg="#0d2438",
            fg="#f0c040"
        ).pack()

        tk.Label(
            header,
            text="Système d'Arbitrage des Candidatures Présidentielles",
            font=("Arial", 11),
            bg="#0d2438",
            fg="white"
        ).pack()

    # ─────────────── FORMULAIRE ───────────────
    def _creer_formulaire(self):
        frame = tk.LabelFrame(
            self.root,
            text="  📋 Informations du Candidat  ",
            font=("Arial", 11, "bold"),
            bg="#1a3a5c",
            fg="white",
            padx=15,
            pady=10
        )
        frame.pack(fill="x", padx=20, pady=10)

        champs = [
            ("Nom", "nom"),
            ("Prénom", "prenom"),
            ("Date de naissance (JJ/MM/AAAA)", "date_naissance"),
            ("Lieu de naissance", "lieu_naissance"),
            ("Nationalité", "nationalite"),
            ("Numéro d'identification nationale", "nin"),
        ]

        self.entries = {}

        for i, (label, key) in enumerate(champs):
            row = i // 2
            col = (i % 2) * 2

            tk.Label(
                frame,
                text=label + " :",
                font=("Arial", 10),
                bg="#1a3a5c",
                fg="white",
                anchor="w"
            ).grid(row=row, column=col, sticky="w", padx=10, pady=5)

            entry = tk.Entry(frame, font=("Arial", 10), width=25, relief="flat",
                             bg="#d0e8ff", fg="#0d2438")
            entry.grid(row=row, column=col + 1, sticky="w", padx=10, pady=5)
            self.entries[key] = entry

        # Champ fichier parrainage
        tk.Label(
            frame,
            text="Fichier de parrainage :",
            font=("Arial", 10),
            bg="#1a3a5c",
            fg="white",
            anchor="w"
        ).grid(row=3, column=0, sticky="w", padx=10, pady=5)

        fichier_frame = tk.Frame(frame, bg="#1a3a5c")
        fichier_frame.grid(row=3, column=1, sticky="w", padx=10)

        self.label_fichier = tk.Label(
            fichier_frame,
            text="Aucun fichier sélectionné",
            font=("Arial", 9, "italic"),
            bg="#1a3a5c",
            fg="#aaaaaa"
        )
        self.label_fichier.pack(side="left")

        tk.Button(
            fichier_frame,
            text="📂 Importer",
            font=("Arial", 9, "bold"),
            bg="#f0c040",
            fg="#0d2438",
            relief="flat",
            cursor="hand2",
            command=self._importer_parrainage
        ).pack(side="left", padx=5)

    # ─────────────── BOUTONS ───────────────
    def _creer_boutons(self):
        frame = tk.Frame(self.root, bg="#1a3a5c", pady=5)
        frame.pack()

        tk.Button(
            frame,
            text="✅ Vérifier la Candidature",
            font=("Arial", 12, "bold"),
            bg="#27ae60",
            fg="white",
            relief="flat",
            padx=20,
            pady=8,
            cursor="hand2",
            command=self._verifier
        ).grid(row=0, column=0, padx=10)

        tk.Button(
            frame,
            text="🗑️ Effacer",
            font=("Arial", 12, "bold"),
            bg="#e74c3c",
            fg="white",
            relief="flat",
            padx=20,
            pady=8,
            cursor="hand2",
            command=self._effacer
        ).grid(row=0, column=1, padx=10)

    # ─────────────── ZONE RÉSULTATS ───────────────
    def _creer_zone_resultats(self):
        frame = tk.LabelFrame(
            self.root,
            text="  📊 Résultat de la Vérification  ",
            font=("Arial", 11, "bold"),
            bg="#1a3a5c",
            fg="white",
            padx=15,
            pady=10
        )
        frame.pack(fill="x", padx=20, pady=5)

        self.label_resultat = tk.Label(
            frame,
            text="En attente de vérification...",
            font=("Arial", 13, "bold"),
            bg="#1a3a5c",
            fg="#aaaaaa"
        )
        self.label_resultat.pack(pady=5)

        self.label_details = tk.Label(
            frame,
            text="",
            font=("Arial", 10),
            bg="#1a3a5c",
            fg="white",
            justify="left"
        )
        self.label_details.pack(pady=3)

    # ─────────────── DASHBOARD ───────────────
    def _creer_dashboard(self):
        frame = tk.LabelFrame(
            self.root,
            text="  📈 Tableau de Bord - Statistiques  ",
            font=("Arial", 11, "bold"),
            bg="#1a3a5c",
            fg="white",
            padx=15,
            pady=10
        )
        frame.pack(fill="both", expand=True, padx=20, pady=5)

        # Stats
        stats_frame = tk.Frame(frame, bg="#1a3a5c")
        stats_frame.pack(fill="x", pady=5)

        self.stat_total = self._carte_stat(stats_frame, "Total", "0", "#3498db")
        self.stat_accepte = self._carte_stat(stats_frame, "✅ Acceptées", "0", "#27ae60")
        self.stat_rejete = self._carte_stat(stats_frame, "❌ Rejetées", "0", "#e74c3c")

        # Tableau historique
        colonnes = ("Nom", "Prénom", "Nationalité", "Âge", "Parrainage", "Résultat")
        self.tableau = ttk.Treeview(frame, columns=colonnes, show="headings", height=5)

        for col in colonnes:
            self.tableau.heading(col, text=col)
            self.tableau.column(col, width=120, anchor="center")

        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.tableau.yview)
        self.tableau.configure(yscroll=scrollbar.set)

        self.tableau.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Style tableau
        style = ttk.Style()
        style.configure("Treeview", background="#d0e8ff", foreground="#0d2438",
                        rowheight=25, fieldbackground="#d0e8ff")
        style.configure("Treeview.Heading", background="#0d2438", foreground="white",
                        font=("Arial", 10, "bold"))

    def _carte_stat(self, parent, titre, valeur, couleur):
        frame = tk.Frame(parent, bg=couleur, padx=20, pady=10, relief="flat")
        frame.pack(side="left", expand=True, fill="x", padx=5)

        tk.Label(frame, text=titre, font=("Arial", 10), bg=couleur, fg="white").pack()
        label = tk.Label(frame, text=valeur, font=("Arial", 18, "bold"), bg=couleur, fg="white")
        label.pack()
        return label

    # ─────────────── ACTIONS ───────────────
    def _importer_parrainage(self):
        fichier = filedialog.askopenfilename(
            title="Sélectionner le fichier de parrainage",
            filetypes=[("Fichiers Excel/CSV", "*.xlsx *.xls *.csv"), ("Tous", "*.*")]
        )
        if fichier:
            self.fichier_parrainage = fichier
            nom_court = os.path.basename(fichier)
            self.label_fichier.config(text=f"✅ {nom_court}", fg="#27ae60")

    def _verifier(self):
        # Récupérer les données du formulaire
        donnees = {k: v.get().strip() for k, v in self.entries.items()}

        # Vérification des champs vides
        for key, val in donnees.items():
            if not val:
                messagebox.showwarning("Champ manquant", f"Veuillez remplir le champ : {key}")
                return

        if not self.fichier_parrainage:
            messagebox.showwarning("Fichier manquant", "Veuillez importer le fichier de parrainage.")
            return

        # Calcul de l'âge
        try:
            date_naissance = datetime.strptime(donnees["date_naissance"], "%d/%m/%Y")
            today = datetime.today()
            age = today.year - date_naissance.year - (
                (today.month, today.day) < (date_naissance.month, date_naissance.day)
            )
        except ValueError:
            messagebox.showerror("Erreur", "Format de date invalide. Utilisez JJ/MM/AAAA")
            return

        # Tentative de connexion avec le backend des camarades
        try:
            from utils.excel_reader import lire_fichier_excel
            from utils.logique_verification import verifier_parrainage

            nb_parrains = lire_fichier_excel(self.fichier_parrainage)
            resultat_parrainage = verifier_parrainage(nb_parrains)
        except Exception:
            # Si le backend n'est pas encore prêt, simulation
            resultat_parrainage = True
            nb_parrains = "Non calculé"

        # Vérifications
        age_ok = age >= 35
        nationalite_ok = donnees["nationalite"].lower() in ("sénégalaise", "senegalaise")

        # Résultat final
        if age_ok and nationalite_ok and resultat_parrainage:
            statut = "✅ CANDIDATURE ACCEPTÉE"
            couleur = "#27ae60"
            details = f"Âge : {age} ans ✅ | Nationalité : {donnees['nationalite']} ✅ | Parrainage : ✅"
        else:
            statut = "❌ CANDIDATURE REJETÉE"
            couleur = "#e74c3c"
            raisons = []
            if not age_ok:
                raisons.append(f"Âge insuffisant ({age} ans, minimum 35)")
            if not nationalite_ok:
                raisons.append("Nationalité non sénégalaise")
            if not resultat_parrainage:
                raisons.append("Parrainage invalide")
            details = " | ".join(raisons)

        # Affichage résultat
        self.label_resultat.config(text=statut, fg=couleur)
        self.label_details.config(text=details)

        # Ajout au tableau et stats
        self.resultats.append(statut)
        self.tableau.insert("", "end", values=(
            donnees["nom"], donnees["prenom"],
            donnees["nationalite"], age,
            os.path.basename(self.fichier_parrainage),
            statut
        ))

        total = len(self.resultats)
        acceptes = sum(1 for r in self.resultats if "ACCEPTÉE" in r)
        rejetes = total - acceptes

        self.stat_total.config(text=str(total))
        self.stat_accepte.config(text=str(acceptes))
        self.stat_rejete.config(text=str(rejetes))

    def _effacer(self):
        for entry in self.entries.values():
            entry.delete(0, tk.END)
        self.fichier_parrainage = None
        self.label_fichier.config(text="Aucun fichier sélectionné", fg="#aaaaaa")
        self.label_resultat.config(text="En attente de vérification...", fg="#aaaaaa")
        self.label_details.config(text="")


# ─────────────── LANCEMENT ───────────────
if __name__ == "__main__":
    root = tk.Tk()
    app = AppCandidature(root)
    root.mainloop()