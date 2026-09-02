import tkinter as tk
from tkinter import messagebox

from database import get_connection
from register import RegisterWindow
from dashboard import Dashboard


class LoginWindow:

    def __init__(self, root):

        self.root = root
        self.root.title("WhatsApp Management System - Login")
        self.root.geometry("450x400")
        self.root.resizable(False, False)

        title = tk.Label(
            root,
            text="WhatsApp Management System",
            font=("Arial", 20, "bold")
        )
        title.pack(pady=30)

        tk.Label(
            root,
            text="Username",
            font=("Arial", 12)
        ).pack()

        self.username_entry = tk.Entry(
            root,
            width=30,
            font=("Arial", 12)
        )
        self.username_entry.pack(pady=5)

        tk.Label(
            root,
            text="Password",
            font=("Arial", 12)
        ).pack()

        self.password_entry = tk.Entry(
            root,
            width=30,
            show="*",
            font=("Arial", 12)
        )
        self.password_entry.pack(pady=5)

        tk.Button(
            root,
            text="Login",
            width=20,
            command=self.login
        ).pack(pady=20)

        tk.Button(
            root,
            text="Create New Account",
            width=20,
            command=self.open_register
        ).pack()

    def login(self):

        username = self.username_entry.get()
        password = self.password_entry.get()

        if username == "" or password == "":
            messagebox.showwarning(
                "Warning",
                "Please enter username and password."
            )
            return

        conn = get_connection()

        if conn is None:
            messagebox.showerror(
                "Database Error",
                "Could not connect to Oracle database."
            )
            return

        cursor = conn.cursor()

        try:

            cursor.execute(
                """
                SELECT user_id, username, full_name
                FROM users
                WHERE username = :username
                AND password = :password
                """,
                {
                    "username": username,
                    "password": password
                }
            )

            user = cursor.fetchone()

            if user:

                self.root.withdraw()

                Dashboard(
                    self.root,
                    user[0],
                    user[1],
                    user[2]
                )

            else:

                messagebox.showerror(
                    "Login Failed",
                    "Invalid username or password."
                )

        except Exception as e:

            messagebox.showerror(
                "Error",
                str(e)
            )

        finally:

            cursor.close()
            conn.close()

    def open_register(self):

        RegisterWindow(self.root)