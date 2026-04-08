from backend.gestion_db import initialiser_db
from Ui import AppCandidature
import tkinter as tk

def main():
    initialiser_db()

    root = tk.Tk()
    app = AppCandidature(root)
    root.mainloop()

if __name__ == "__main__":
    main()