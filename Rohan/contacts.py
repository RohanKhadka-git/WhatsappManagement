import tkinter as tk
from tkinter import ttk, messagebox

from database import get_connection


class ContactsWindow:

    def __init__(self, parent, user_id):

        self.user_id = user_id

        self.window = tk.Toplevel(parent)

        self.window.title("Contact Management")
        self.window.geometry("800x600")

        tk.Label(
            self.window,
            text="Contact Management",
            font=("Arial", 20, "bold")
        ).pack(pady=15)

        form = tk.Frame(self.window)

        form.pack(pady=10)

        tk.Label(form, text="Name").grid(
            row=0,
            column=0,
            padx=5,
            pady=5
        )

        self.name_entry = tk.Entry(form)

        self.name_entry.grid(
            row=0,
            column=1
        )

        tk.Label(form, text="Phone").grid(
            row=1,
            column=0,
            padx=5,
            pady=5
        )

        self.phone_entry = tk.Entry(form)

        self.phone_entry.grid(
            row=1,
            column=1
        )

        tk.Label(form, text="Email").grid(
            row=2,
            column=0,
            padx=5,
            pady=5
        )

        self.email_entry = tk.Entry(form)

        self.email_entry.grid(
            row=2,
            column=1
        )

        tk.Button(
            form,
            text="Add Contact",
            command=self.add_contact
        ).grid(
            row=3,
            column=0,
            columnspan=2,
            pady=10
        )

        columns = (
            "ID",
            "Name",
            "Phone",
            "Email"
        )

        self.tree = ttk.Treeview(
            self.window,
            columns=columns,
            show="headings"
        )

        for column in columns:

            self.tree.heading(
                column,
                text=column
            )

            self.tree.column(
                column,
                width=150
            )

        self.tree.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

        buttons = tk.Frame(self.window)

        buttons.pack(pady=10)

        tk.Button(
            buttons,
            text="Delete Contact",
            command=self.delete_contact
        ).pack(
            side="left",
            padx=10
        )

        tk.Button(
            buttons,
            text="Refresh",
            command=self.load_contacts
        ).pack(
            side="left",
            padx=10
        )

        self.load_contacts()

    def add_contact(self):

        name = self.name_entry.get()
        phone = self.phone_entry.get()
        email = self.email_entry.get()

        if not name or not phone:

            messagebox.showwarning(
                "Warning",
                "Name and phone are required."
            )

            return

        conn = get_connection()

        if conn is None:
            return

        cursor = conn.cursor()

        try:

            cursor.execute(
                """
                INSERT INTO contacts
                (user_id, contact_name, phone, email)
                VALUES
                (:user_id, :name, :phone, :email)
                """,
                {
                    "user_id": self.user_id,
                    "name": name,
                    "phone": phone,
                    "email": email
                }
            )

            conn.commit()

            messagebox.showinfo(
                "Success",
                "Contact added successfully."
            )

            self.name_entry.delete(0, tk.END)
            self.phone_entry.delete(0, tk.END)
            self.email_entry.delete(0, tk.END)

            self.load_contacts()

        except Exception as e:

            conn.rollback()

            messagebox.showerror(
                "Error",
                str(e)
            )

        finally:

            cursor.close()
            conn.close()

    def load_contacts(self):

        for item in self.tree.get_children():

            self.tree.delete(item)

        conn = get_connection()

        if conn is None:
            return

        cursor = conn.cursor()

        try:

            cursor.execute(
                """
                SELECT contact_id,
                       contact_name,
                       phone,
                       email
                FROM contacts
                WHERE user_id = :user_id
                ORDER BY contact_id
                """,
                {
                    "user_id": self.user_id
                }
            )

            rows = cursor.fetchall()

            for row in rows:

                self.tree.insert(
                    "",
                    tk.END,
                    values=row
                )

        finally:

            cursor.close()
            conn.close()

    def delete_contact(self):

        selected = self.tree.selection()

        if not selected:

            messagebox.showwarning(
                "Warning",
                "Select a contact first."
            )

            return

        values = self.tree.item(
            selected[0],
            "values"
        )

        contact_id = values[0]

        conn = get_connection()

        if conn is None:
            return

        cursor = conn.cursor()

        try:

            cursor.execute(
                """
                DELETE FROM contacts
                WHERE contact_id = :id
                """,
                {
                    "id": contact_id
                }
            )

            conn.commit()

            messagebox.showinfo(
                "Success",
                "Contact deleted."
            )

            self.load_contacts()

        except Exception as e:

            conn.rollback()

            messagebox.showerror(
                "Error",
                str(e)
            )

        finally:

            cursor.close()
            conn.close()