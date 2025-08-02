import tkinter as tk
from tkinter import messagebox
import sqlite3

# Database setup
def init_db():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Register function
def register_user():
    username = reg_username.get()
    password = reg_password.get()

    if not username or not password:
        messagebox.showerror("Error", "All fields are required")
        return

    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        messagebox.showinfo("Success", "Registration successful")
        reg_username.delete(0, tk.END)
        reg_password.delete(0, tk.END)
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Username already exists")
    conn.close()

# Login function
def login_user():
    username = login_username.get()
    password = login_password.get()

    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    result = cursor.fetchone()
    conn.close()

    if result:
        messagebox.showinfo("Success", "Login successful")
    else:
        messagebox.showerror("Error", "Invalid username or password")

# GUI setup
root = tk.Tk()
root.title("Login & Register Page")
root.geometry("400x400")
root.resizable(False, False)

# Register Frame
reg_frame = tk.LabelFrame(root, text="Register", padx=10, pady=10)
reg_frame.pack(padx=10, pady=10, fill="x")

tk.Label(reg_frame, text="Username").pack()
reg_username = tk.Entry(reg_frame)
reg_username.pack()

tk.Label(reg_frame, text="Password").pack()
reg_password = tk.Entry(reg_frame, show="*")
reg_password.pack()

tk.Button(reg_frame, text="Register", command=register_user).pack(pady=5)

# Login Frame
login_frame = tk.LabelFrame(root, text="Login", padx=10, pady=10)
login_frame.pack(padx=10, pady=10, fill="x")

tk.Label(login_frame, text="Username").pack()
login_username = tk.Entry(login_frame)
login_username.pack()

tk.Label(login_frame, text="Password").pack()
login_password = tk.Entry(login_frame, show="*")
login_password.pack()

tk.Button(login_frame, text="Login", command=login_user).pack(pady=5)

# Initialize DB and run GUI
init_db()
root.mainloop()
