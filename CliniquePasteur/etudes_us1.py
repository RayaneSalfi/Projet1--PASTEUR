import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from mysql.connector import Error
import sys


HOST = "172.27.0.50"
USER = "grp03Admin"
PASSWORD = "grp03Mdp"
DATABASE = "grp03ClinPasteur"


class Database:
    """Connexion MySQL pour la page des études."""
    
    def __init__(self):
        try:
            self.conn = mysql.connector.connect(
                host=HOST, user=USER, password=PASSWORD, database=DATABASE
            )
            self.cursor = self.conn.cursor(dictionary=True)
            print("Connexion OK (études)")
        except Error as e:
            messagebox.showerror("Erreur DB", f"Impossible de se connecter : {e}")
            self.conn = None

    def get_etudes(self):
        if not self.conn: return []
        sql = """
        SELECT 
            nomEtu AS nom,
            descEtude AS description,
            NULL AS type,
            NULL AS date_fin
        FROM etudes
        """
        try:
            self.cursor.execute(sql)
            return self.cursor.fetchall()
        except Error:
            return []

    def close(self):
        if self.cursor: self.cursor.close()
        if self.conn: self.conn.close()


class EtudesListApp(tk.Toplevel):
    """Fenêtre d'affichage des études."""
    
    def __init__(self, parent):
        super().__init__(parent)
        parent.withdraw()

        self.title("Études en cours")
        self.geometry("800x500")

        self.db = Database()

        tk.Label(self, text="Études disponibles",
                 font=('Arial', 24, 'bold')).pack(pady=20)

        self.tree = ttk.Treeview(
            self, columns=("nom", "description", "type", "date_fin"), show="headings"
        )
        self.tree.heading("nom", text="Nom")
        self.tree.heading("description", text="Description")
        self.tree.heading("type", text="Type")
        self.tree.heading("date_fin", text="Date de fin")

        self.tree.column("nom", width=150)
        self.tree.column("description", width=350)
        self.tree.column("type", width=120)
        self.tree.column("date_fin", width=120)

        self.tree.pack(expand=True, fill="both")

        tk.Button(self, text="Retour",
                 bg="#6A5ACD", fg="white",
                 font=('Arial', 12, 'bold'),
                 command=self.go_back).pack(pady=10)

        self.load_data()

    def load_data(self):
        etudes = self.db.get_etudes()
        if not etudes:
            messagebox.showinfo("Info", "Aucune étude disponible.")
            self.go_back()
            return
        
        for e in etudes:
            self.tree.insert("", "end", values=(
                e["nom"], e["description"], e["type"] or "N/A", e["date_fin"] or "N/A"
            ))

    def go_back(self):
        self.db.close()
        self.master.deiconify()
        self.destroy()
