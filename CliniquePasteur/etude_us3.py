import tkinter as tk
from tkinter import messagebox
import mysql.connector
from mysql.connector import Error


HOST = "172.27.0.50"
USER = "grp03Admin"
PASSWORD = "grp03Mdp"
DATABASE = "grp03ClinPasteur"


class Database:
    """Gestion MySQL pour l'ajout d'études."""

    def __init__(self):
        try:
            self.conn = mysql.connector.connect(
                host=HOST, user=USER, password=PASSWORD, database=DATABASE
            )
            self.cursor = self.conn.cursor()
            print("DB OK (add étude)")
        except Error as e:
            messagebox.showerror("Erreur SQL", f"{e}")
            self.conn = None

    def insert_etude(self, nom, description, protocole, question, organisme, date):
        if not self.conn:
            return False

        sql = """
        INSERT INTO etudes (nomEtu, descEtude, idProtocole, idQuestion, idOrganisme, dateDebEtu)
        VALUES (%s, %s, %s, %s, %s, %s)
        """

        try:
            self.cursor.execute(sql, (nom, description, protocole, question, organisme, date))
            self.conn.commit()
            return True
        except Error as e:
            messagebox.showerror("Erreur SQL", f"{e}")
            return False

    def close(self):
        if self.cursor: self.cursor.close()
        if self.conn: self.conn.close()


class AddEtudeWindow(tk.Toplevel):
    """Fenêtre de création d’une nouvelle étude."""

    def __init__(self, parent):
        super().__init__(parent)
        self.title("Nouvelle Étude")
        self.geometry("450x500")

        self.db = Database()

        tk.Label(self, text="Créer une nouvelle étude",
                 font=("Arial", 20, "bold")).pack(pady=15)

        # Champs du formulaire
        self.entry_nom = self.create_entry("Nom de l'étude :")
        self.entry_desc = self.create_entry("Description :")
        self.entry_protocole = self.create_entry("ID Protocole :")
        self.entry_question = self.create_entry("ID Question :")
        self.entry_organisme = self.create_entry("ID Organisme :")
        self.entry_date = self.create_entry("Date (AAAA-MM-JJ) :")

        tk.Button(self, text="Enregistrer",
                  bg="#4CAF50", fg="white", font=("Arial", 12, "bold"),
                  command=self.save_etude).pack(pady=15)

        tk.Button(self, text="Annuler",
                  bg="#B22222", fg="white", font=("Arial", 12),
                  command=self.close_window).pack()

    def create_entry(self, label_text):
        frame = tk.Frame(self)
        frame.pack(pady=5)

        tk.Label(frame, text=label_text,
                 font=("Arial", 12)).pack(anchor="w")

        entry = tk.Entry(frame, width=40)
        entry.pack()
        return entry

    def save_etude(self):
        nom = self.entry_nom.get().strip()
        description = self.entry_desc.get().strip()
        protocole = self.entry_protocole.get().strip()
        question = self.entry_question.get().strip()
        organisme = self.entry_organisme.get().strip()
        date = self.entry_date.get().strip()

        # Validation
        if not all([nom, description, protocole, question, organisme, date]):
            messagebox.showwarning("Champs manquants", "Veuillez remplir tous les champs.")
            return

        if self.db.insert_etude(nom, description, protocole, question, organisme, date):
            messagebox.showinfo("Succès", "Étude enregistrée avec succès.")
            self.close_window()

    def close_window(self):
        self.db.close()
        self.destroy()
