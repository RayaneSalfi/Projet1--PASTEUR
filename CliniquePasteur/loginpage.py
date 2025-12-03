import tkinter as tk
from tkinter import messagebox
import mysql.connector
from mysql.connector import Error
import random
from datetime import datetime, timedelta
import sys

from etude_us3 import AddEtudeWindow

HOST = "172.27.0.50"
USER = "grp03Admin"
PASSWORD = "grp03Mdp"
DATABASE = "grp03ClinPasteur"


class Database:
    """Gère la connexion et les opérations MySQL."""
    
    def __init__(self, host, user, password, database):
        self.conn = None
        self.cursor = None
        self.connect_info = {
            'host': host,
            'user': user,
            'password': password,
            'database': database
        }
        self.connect()

    def connect(self):
        """Tente de se connecter à MySQL."""
        try:
            self.conn = mysql.connector.connect(**self.connect_info)
            if self.conn.is_connected():
                print("Connexion MySQL OK.")
                self.cursor = self.conn.cursor(dictionary=True)
        except Error as e:
            messagebox.showerror("Erreur DB", f"Connexion impossible : {e}")

    def is_connected(self):
        return self.conn is not None and self.conn.is_connected()

    def verify_login(self, email, password):
        """Vérifie email + mot de passe."""
        if not self.is_connected():
            return None
        
        sql = "SELECT id, role FROM Clients WHERE email = %s AND motDePasse = %s"
        try:
            self.cursor.execute(sql, (email, password))
            return self.cursor.fetchone()
        except:
            return None

    def execute(self, sql, params=None):
        """Exécute un UPDATE/DELETE/INSERT."""
        try:
            self.cursor.execute(sql, params or ())
            self.conn.commit()
            return True
        except Error as e:
            messagebox.showerror("Erreur SQL", f"{e}")
            return False

    def set_otp(self, user_id, otp_code, expiration_time):
        """Stocke l’OTP."""
        sql = "UPDATE Clients SET otp_code=%s, otp_expiration=%s WHERE id=%s"
        return self.execute(sql, (otp_code, expiration_time, user_id))

    def verify_otp(self, user_id, submitted_otp):
        """Vérifie que l’OTP correspond et n’est pas expiré."""
        sql = """
        SELECT COUNT(*) AS nb
        FROM Clients
        WHERE id=%s AND otp_code=%s AND otp_expiration > NOW()
        """
        try:
            self.cursor.execute(sql, (user_id, submitted_otp))
            result = self.cursor.fetchone()
            if result['nb'] == 1:
                self.clear_otp(user_id)
                return True
            return False
        except:
            return False

    def clear_otp(self, user_id):
        sql = "UPDATE Clients SET otp_code=NULL, otp_expiration=NULL WHERE id=%s"
        self.execute(sql, (user_id,))

    def close(self):
        if self.cursor: self.cursor.close()
        if self.conn: self.conn.close()



#OTP
def generate_otp():
    """Génère un OTP à 6 chiffres."""
    return str(random.randint(100000, 999999))

def open_otp_window(user_id, login_window, user_info, db):
    """Ouvre une fenêtre pour saisir l’OTP."""
    
    otp_window = tk.Toplevel(login_window)
    otp_window.title("Vérification OTP")
    otp_window.geometry("300x160")

    tk.Label(otp_window, text="Veuillez entrer le code OTP :", font=('Arial', 11)).pack(pady=10)
    otp_entry = tk.Entry(otp_window, show='*', width=20)
    otp_entry.pack(pady=5)

    def submit():
        otp = otp_entry.get().strip()
        if db.verify_otp(user_id, otp):
            otp_window.destroy()
            open_main_interface(user_info)
        else:
            messagebox.showerror("Erreur", "Code incorrect ou expiré.")
            login_window.deiconify()
            otp_window.destroy()

    tk.Button(otp_window, text="Valider", command=submit).pack(pady=10)




def open_etudes_module(parent):
    """Importe et ouvre la page des études."""
    from etudes_us1 import EtudesListApp
    EtudesListApp(parent)

def open_main_interface(user_info):
    """Ouvre le tableau de bord principal."""
    
    role = user_info['role'].lower().strip()
    
    dashboard = tk.Tk()
    dashboard.title("Tableau de Bord")
    dashboard.geometry("500x350")

    tk.Label(dashboard, text=f"Bienvenue, {role} !",
             font=('Arial', 18, 'bold')).pack(pady=20)

    # Accès médecin et assistant
    if role in ["medecin", "assistant"]:

        # Voir les études
        tk.Button(
            dashboard,
            text="Voir les études",
            font=('Arial', 12, 'bold'),
            bg='#6A5ACD', fg='white',
            padx=10, pady=5,
            command=lambda: open_etudes_module(dashboard)
        ).pack(pady=10)

        # Ajouter une étude
        tk.Button(
            dashboard,
            text="Ajouter une étude",
            font=('Arial', 12, 'bold'),
            bg='#4CAF50', fg='white',
            padx=10, pady=5,
            command=lambda: AddEtudeWindow(dashboard)
        ).pack(pady=10)

    dashboard.mainloop()



#LOGIN PAGE

db = Database(HOST, USER, PASSWORD, DATABASE)

Window = tk.Tk()
Window.title("Connexion 2FA")
Window.geometry("340x200")

tk.Label(Window, text="Connexion", font=('Arial', 16, 'bold')).grid(row=0, column=0, columnspan=2, pady=10)

tk.Label(Window, text="Email :").grid(row=1, column=0, sticky='w')
Email_entry = tk.Entry(Window)
Email_entry.grid(row=1, column=1)

tk.Label(Window, text="Mot de passe :").grid(row=2, column=0, sticky='w')
MotDePasse_entry = tk.Entry(Window, show='*')
MotDePasse_entry.grid(row=2, column=1)


def verification_login():
    email = Email_entry.get()
    mdp = MotDePasse_entry.get()

    if not email or not mdp:
        messagebox.showwarning("Attention", "Champs manquants.")
        return

    user_info = db.verify_login(email, mdp)

    if not user_info:
        messagebox.showerror("Erreur", "Email ou mot de passe incorrect.")
        return

    otp = generate_otp()
    expiration = datetime.now() + timedelta(minutes=5)

    db.set_otp(user_info['id'], otp, expiration)

    print(f"\n=== CODE OTP POUR {email} ===")
    print("OTP :", otp)
    print("Valable jusqu'à :", expiration.strftime("%H:%M:%S"))
    print("==============================\n")

    Window.withdraw()
    open_otp_window(user_info['id'], Window, user_info, db)


tk.Button(Window, text="Connexion", command=verification_login).grid(row=3, column=0, columnspan=2, pady=10)

Window.mainloop()
db.close()
