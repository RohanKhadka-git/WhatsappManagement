import tkinter as tk
from tkinter import messagebox

from database import get_connection


class RegisterWindow:

    def __init__(self, parent):

        self.window = tk.Toplevel(parent)

        self.window.title("Create Account")
        self.window.geometry("450x500")
        self.window.resizable(False, False)

        tk.Label(
            self.window,
            text="Create New Account",
            font=("Arial", 20, "bold")
        ).pack(pady=20)

        tk.Label(self.window, text="Full Name").pack()

        self.name_entry = tk.Entry(
            self.window,
            width=35
        )
        self.name_entry.pack(pady=5)

        tk.Label(self.window, text="Username").pack()

        self.username_entry = tk.Entry(
            self.window,
            width=35
        )
        self.username_entry.pack(pady=5)

        tk.Label(self.window, text="Phone Number").pack()

        self.phone_entry = tk.Entry(
            self.window,
            width=35
        )
        self.phone_entry.pack(pady=5)

        tk.Label(self.window, text="Password").pack()

        self.password_entry = tk.Entry(
            self.window,
            width=35,
            show="*"
        )
        self.password_entry.pack(pady=5)

        tk.Button(
            self.window,
            text="Register",
            width=20,
            command=self.register
        ).pack(pady=25)

    def register(self):

        name = self.name_entry.get()
        username = self.username_entry.get()
        phone = self.phone_entry.get()
        password = self.password_entry.get()

        if not name or not username or not phone or not password:

            messagebox.showwarning(
                "Warning",
                "All fields are required."
            )

            return

        conn = get_connection()

        if conn is None:

            messagebox.showerror(
                "Error",
                "Database connection failed."
            )

            return

        cursor = conn.cursor()

        try:

            cursor.execute(
                """
                INSERT INTO users
                (username, password, phone, full_name)
                VALUES
                (:username, :password, :phone, :name)
                """,
                {
                    "username": username,
                    "password": password,
                    "phone": phone,
                    "name": name
                }
            )

            conn.commit()

            messagebox.showinfo(
                "Success",
                "Account created successfully!"
            )

            self.window.destroy()

        except Exception as e:

            conn.rollback()

            messagebox.showerror(
                "Registration Error",
                str(e)
            )

        finally:

            cursor.close()
            conn.close()