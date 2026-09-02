import tkinter as tk
from tkinter import ttk, messagebox

from database import get_connection


class MessagesWindow:

    def __init__(self, parent, user_id):

        self.user_id = user_id

        self.window = tk.Toplevel(parent)

        self.window.title("Message Management")
        self.window.geometry("900x650")

        tk.Label(
            self.window,
            text="Message Management",
            font=("Arial", 20, "bold")
        ).pack(pady=15)

        form = tk.Frame(self.window)

        form.pack(pady=10)

        tk.Label(
            form,
            text="Receiver Username"
        ).grid(
            row=0,
            column=0,
            padx=5,
            pady=5
        )

        self.receiver_entry = tk.Entry(
            form,
            width=30
        )

        self.receiver_entry.grid(
            row=0,
            column=1
        )

        tk.Label(
            form,
            text="Message"
        ).grid(
            row=1,
            column=0,
            padx=5,
            pady=5
        )

        self.message_entry = tk.Entry(
            form,
            width=50
        )

        self.message_entry.grid(
            row=1,
            column=1
        )

        tk.Button(
            form,
            text="Send Message",
            command=self.send_message
        ).grid(
            row=2,
            column=0,
            columnspan=2,
            pady=10
        )

        columns = (
            "ID",
            "Sender",
            "Receiver",
            "Message",
            "Time"
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

        self.tree.column("ID", width=50)
        self.tree.column("Sender", width=120)
        self.tree.column("Receiver", width=120)
        self.tree.column("Message", width=350)
        self.tree.column("Time", width=150)

        self.tree.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

        tk.Button(
            self.window,
            text="Delete Selected Message",
            command=self.delete_message
        ).pack(pady=10)

        self.load_messages()

    def send_message(self):

        receiver = self.receiver_entry.get()
        message = self.message_entry.get()

        if not receiver or not message:

            messagebox.showwarning(
                "Warning",
                "Receiver and message are required."
            )

            return

        conn = get_connection()

        if conn is None:
            return

        cursor = conn.cursor()

        try:

            cursor.execute(
                """
                SELECT user_id
                FROM users
                WHERE username = :username
                """,
                {
                    "username": receiver
                }
            )

            receiver_data = cursor.fetchone()

            if receiver_data is None:

                messagebox.showerror(
                    "Error",
                    "Receiver username does not exist."
                )

                return

            receiver_id = receiver_data[0]

            cursor.execute(
                """
                INSERT INTO messages
                (sender_id, receiver_id, message_text)
                VALUES
                (:sender, :receiver, :message)
                """,
                {
                    "sender": self.user_id,
                    "receiver": receiver_id,
                    "message": message
                }
            )

            conn.commit()

            messagebox.showinfo(
                "Success",
                "Message sent successfully."
            )

            self.receiver_entry.delete(
                0,
                tk.END
            )

            self.message_entry.delete(
                0,
                tk.END
            )

            self.load_messages()

        except Exception as e:

            conn.rollback()

            messagebox.showerror(
                "Error",
                str(e)
            )

        finally:

            cursor.close()
            conn.close()

    def load_messages(self):

        for item in self.tree.get_children():

            self.tree.delete(item)

        conn = get_connection()

        if conn is None:
            return

        cursor = conn.cursor()

        try:

            cursor.execute(
                """
                SELECT
                    m.message_id,
                    u1.username AS sender,
                    u2.username AS receiver,
                    m.message_text,
                    m.sent_time
                FROM messages m
                JOIN users u1
                    ON m.sender_id = u1.user_id
                JOIN users u2
                    ON m.receiver_id = u2.user_id
                WHERE
                    m.sender_id = :user_id
                    OR m.receiver_id = :user_id
                ORDER BY m.sent_time DESC
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

    def delete_message(self):

        selected = self.tree.selection()

        if not selected:

            messagebox.showwarning(
                "Warning",
                "Select a message first."
            )

            return

        values = self.tree.item(
            selected[0],
            "values"
        )

        message_id = values[0]

        conn = get_connection()

        if conn is None:
            return

        cursor = conn.cursor()

        try:

            cursor.execute(
                """
                DELETE FROM messages
                WHERE message_id = :id
                AND sender_id = :user_id
                """,
                {
                    "id": message_id,
                    "user_id": self.user_id
                }
            )

            conn.commit()

            self.load_messages()

        except Exception as e:

            conn.rollback()

            messagebox.showerror(
                "Error",
                str(e)
            )

        finally:

            cursor.close()
            conn.close()