import mysql.connector
from cryptography.fernet import Fernet
import os
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog
import re
import time
import pyotp
import tkinter.font as tkFont

def generate_key():
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)

def load_key():
    return open("secret.key", "rb").read()

if not os.path.exists("secret.key"):
    generate_key()

key = load_key()
cipher_suite = Fernet(key)

def encrypt_password(password):
    return cipher_suite.encrypt(password.encode())

def decrypt_password(encrypted_password):
    return cipher_suite.decrypt(encrypted_password).decode()

# MySQL connection setup
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="ritwick22",
    database="password_manager_db"
)
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS passwords (
                id INT AUTO_INCREMENT PRIMARY KEY,
                website VARCHAR(255) NOT NULL,
                username VARCHAR(255) NOT NULL,
                password TEXT NOT NULL,
                last_changed TIMESTAMP NOT NULL
            )''')
conn.commit()

SECRET = 'JBSWY3DPEHPK3PXP'
totp = pyotp.TOTP(SECRET)

class PasswordManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Password Manager")
        self.root.geometry("400x500")
        
        self.dark_mode = tk.BooleanVar()
        self.font = tkFont.Font(family='Helvetica', size=12)
        
        self.create_widgets()
        self.update_ui()

    def create_widgets(self):
        self.website_label = ttk.Label(self.root, text="Website", font=self.font)
        self.website_entry = ttk.Entry(self.root, font=self.font)

        self.username_label = ttk.Label(self.root, text="Username", font=self.font)
        self.username_entry = ttk.Entry(self.root, font=self.font)

        self.password_label = ttk.Label(self.root, text="Password", font=self.font)
        self.password_entry = ttk.Entry(self.root, show="*", font=self.font)
        self.password_entry.bind("<KeyRelease>", self.check_password_strength)

        self.strength_label = ttk.Label(self.root, text="", font=self.font)

        self.add_button = ttk.Button(self.root, text="Add Password", command=self.add_password)
        self.view_button = ttk.Button(self.root, text="View Passwords", command=self.view_passwords)
        self.search_button = ttk.Button(self.root, text="Search Passwords", command=self.search_passwords)
        self.backup_button = ttk.Button(self.root, text="Backup Passwords", command=self.backup_passwords)
        self.restore_button = ttk.Button(self.root, text="Restore Passwords", command=self.restore_passwords)
        self.dark_mode_check = ttk.Checkbutton(self.root, text="Dark Mode", variable=self.dark_mode, command=self.toggle_dark_mode)

        self.website_label.pack(pady=5)
        self.website_entry.pack(pady=5)
        self.username_label.pack(pady=5)
        self.username_entry.pack(pady=5)
        self.password_label.pack(pady=5)
        self.password_entry.pack(pady=5)
        self.strength_label.pack(pady=5)
        self.add_button.pack(pady=5)
        self.view_button.pack(pady=5)
        self.search_button.pack(pady=5)
        self.backup_button.pack(pady=5)
        self.restore_button.pack(pady=5)
        self.dark_mode_check.pack(pady=5)

    def update_ui(self):
        style = ttk.Style()
        if self.dark_mode.get():
            self.root.configure(bg='black')
            style.configure('TLabel', background='black', foreground='white')
            style.configure('TButton', background='black', foreground='white')
            style.configure('TCheckbutton', background='black', foreground='white')
        else:
            self.root.configure(bg='white')
            style.configure('TLabel', background='white', foreground='black')
            style.configure('TButton', background='white', foreground='black')
            style.configure('TCheckbutton', background='white', foreground='black')
        
        self.website_label.configure(style='TLabel')
        self.username_label.configure(style='TLabel')
        self.password_label.configure(style='TLabel')
        self.strength_label.configure(style='TLabel')

    def check_password_strength(self, event):
        password = self.password_entry.get()
        strength = self.password_strength(password)
        self.strength_label.config(text=strength)

    def password_strength(self, password):
        if len(password) < 6:
            return "Weak"
        if re.search('[0-9]', password) is None:
            return "Weak"
        if re.search('[A-Z]', password) is None:
            return "Medium"
        if re.search('[$#@]', password) is None:
            return "Strong"
        return "Very Strong"

    def add_password(self):
        try:
            website = self.website_entry.get()
            username = self.username_entry.get()
            password = self.password_entry.get()
            encrypted_password = encrypt_password(password)
            c.execute("INSERT INTO passwords (website, username, password, last_changed) VALUES (%s, %s, %s, %s)",
                      (website, username, encrypted_password, time.strftime('%Y-%m-%d %H:%M:%S')))
            conn.commit()
            strength = self.password_strength(password)
            messagebox.showinfo("Success", f"Password added successfully\nStrength: {strength}")
            self.send_2fa_code()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def send_2fa_code(self):
        code = totp.now()
        messagebox.showinfo("2FA Code", f"Your 2FA code is: {code}")

    def view_passwords(self):
        code = simpledialog.askstring("2FA Verification", "Enter 2FA code")
        if totp.verify(code):
            search_term = simpledialog.askstring("Search", "Enter website or username to view")
            if search_term:
                try:
                    c.execute("SELECT * FROM passwords WHERE website LIKE %s OR username LIKE %s", 
                              (f'%{search_term}%', f'%{search_term}%'))
                    rows = c.fetchall()
                    if rows:
                        for row in rows:
                            decrypted_password = decrypt_password(row[3])
                            messagebox.showinfo("Password Info", f"Website: {row[1]}\nUsername: {row[2]}\nPassword: {decrypted_password}\nLast Changed: {row[4]}")
                    else:
                        messagebox.showinfo("No Results", "No passwords found for the given search term.")
                except Exception as e:
                    messagebox.showerror("Error", f"An error occurred: {e}")
        else:
            messagebox.showerror("Error", "Invalid 2FA code")

    def search_passwords(self):
        search_term = simpledialog.askstring("Search", "Enter website or username to search")
        try:
            c.execute("SELECT * FROM passwords WHERE website LIKE %s OR username LIKE %s", (f'%{search_term}%', f'%{search_term}%'))
            rows = c.fetchall()
            for row in rows:
                decrypted_password = decrypt_password(row[3])
                messagebox.showinfo("Password Info", f"Website: {row[1]}\nUsername: {row[2]}\nPassword: {decrypted_password}\nLast Changed: {row[4]}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def backup_passwords(self):
        backup_file = filedialog.asksaveasfilename(defaultextension=".sql", filetypes=[("SQL Dump", "*.sql")])
        if backup_file:
            try:
                os.system(f"mysqldump -u your_username -p your_password password_manager_db > {backup_file}")
                messagebox.showinfo("Success", "Backup completed successfully")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")

    def restore_passwords(self):
        restore_file = filedialog.askopenfilename(defaultextension=".sql", filetypes=[("SQL Dump", "*.sql")])
        if restore_file:
            try:
                os.system(f"mysql -u your_username -p your_password password_manager_db < {restore_file}")
                messagebox.showinfo("Success", "Restore completed successfully")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")

    def toggle_dark_mode(self):
        self.update_ui()

if __name__ == "__main__": 
    root = tk.Tk()
    app = PasswordManager(root)
    root.mainloop()
    conn.close()
