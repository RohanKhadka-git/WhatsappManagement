import tkinter as tk
from tkinter import messagebox

from contacts import ContactsWindow
from messages import MessagesWindow
from groups import GroupsWindow


class Dashboard:

    def __init__(
        self,
        root,
        user_id,
        username,
        full_name
    ):

        self.root = root
        self.user_id = user_id

        self.window = tk.Toplevel(root)

        self.window.title(
            "WhatsApp Management System - Dashboard"
        )

        self.window.geometry("700x550")

        self.window.protocol(
            "WM_DELETE_WINDOW",
            self.logout
        )

        tk.Label(
            self.window,
            text="WhatsApp Management System",
            font=("Arial", 24, "bold")
        ).pack(pady=30)

        tk.Label(
            self.window,
            text=f"Welcome, {full_name}",
            font=("Arial", 14)
        ).pack(pady=10)

        frame = tk.Frame(self.window)

        frame.pack(pady=30)

        tk.Button(
            frame,
            text="Contacts",
            width=20,
            height=2,
            command=self.open_contacts
        ).grid(row=0, column=0, padx=10, pady=10)

        tk.Button(
            frame,
            text="Messages",
            width=20,
            height=2,
            command=self.open_messages
        ).grid(row=0, column=1, padx=10, pady=10)

        tk.Button(
            frame,
            text="Groups",
            width=20,
            height=2,
            command=self.open_groups
        ).grid(row=1, column=0, padx=10, pady=10)

        tk.Button(
            frame,
            text="Logout",
            width=20,
            height=2,
            command=self.logout
        ).grid(row=1, column=1, padx=10, pady=10)

    def open_contacts(self):

        ContactsWindow(
            self.window,
            self.user_id
        )

    def open_messages(self):

        MessagesWindow(
            self.window,
            self.user_id
        )

    def open_groups(self):

        GroupsWindow(
            self.window,
            self.user_id
        )

    def logout(self):

        self.window.destroy()

        self.root.deiconify()