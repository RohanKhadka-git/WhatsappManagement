import tkinter as tk
from tkinter import ttk, messagebox

from database import get_connection


class GroupsWindow:

    def __init__(self, parent, user_id):

        self.user_id = user_id

        self.window = tk.Toplevel(parent)

        self.window.title("Group Management")
        self.window.geometry("800x600")

        tk.Label(
            self.window,
            text="Group Management",
            font=("Arial", 20, "bold")
        ).pack(pady=15)

        form = tk.Frame(self.window)

        form.pack(pady=10)

        tk.Label(
            form,
            text="Group Name"
        ).grid(
            row=0,
            column=0,
            padx=5
        )

        self.group_entry = tk.Entry(
            form,
            width=30
        )

        self.group_entry.grid(
            row=0,
            column=1,
            padx=5
        )

        tk.Button(
            form,
            text="Create Group",
            command=self.create_group
        ).grid(
            row=0,
            column=2,
            padx=10
        )

        columns = (
            "ID",
            "Group Name",
            "Created By",
            "Created At"
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
            "ID",
            width=70
        )

        self.tree.column(
            "Group Name",
            width=200
        )

        self.tree.column(
            "Created By",
            width=150
        )

        self.tree.column(
            "Created At",
            width=200
        )

        self.tree.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

        tk.Button(
            self.window,
            text="Add Selected User to Group",
            command=self.add_member
        ).pack(pady=10)

        self.load_groups()

    def create_group(self):

        group_name = self.group_entry.get()

        if not group_name:

            messagebox.showwarning(
                "Warning",
                "Enter group name."
            )

            return

        conn = get_connection()

        if conn is None:
            return

        cursor = conn.cursor()

        try:

            cursor.execute(
                """
                INSERT INTO whatsapp_groups
                (group_name, created_by)
                VALUES
                (:group_name, :user_id)
                """,
                {
                    "group_name": group_name,
                    "user_id": self.user_id
                }
            )

            conn.commit()

            self.group_entry.delete(
                0,
                tk.END
            )

            messagebox.showinfo(
                "Success",
                "Group created successfully."
            )

            self.load_groups()

        except Exception as e:

            conn.rollback()

            messagebox.showerror(
                "Error",
                str(e)
            )

        finally:

            cursor.close()
            conn.close()

    def load_groups(self):

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
                    g.group_id,
                    g.group_name,
                    u.username,
                    g.created_at
                FROM whatsapp_groups g
                JOIN users u
                    ON g.created_by = u.user_id
                WHERE g.created_by = :user_id
                ORDER BY g.group_id
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

    def add_member(self):

        selected = self.tree.selection()

        if not selected:

            messagebox.showwarning(
                "Warning",
                "Select a group first."
            )

            return

        values = self.tree.item(
            selected[0],
            "values"
        )

        group_id = values[0]

        member_window = tk.Toplevel(
            self.window
        )

        member_window.title(
            "Add Group Member"
        )

        member_window.geometry(
            "350x200"
        )

        tk.Label(
            member_window,
            text="Username"
        ).pack(pady=10)

        username_entry = tk.Entry(
            member_window,
            width=30
        )

        username_entry.pack()

        def save_member():

            username = username_entry.get()

            if not username:

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
                        "username": username
                    }
                )

                user = cursor.fetchone()

                if user is None:

                    messagebox.showerror(
                        "Error",
                        "User does not exist."
                    )

                    return

                cursor.execute(
                    """
                    INSERT INTO group_members
                    (group_id, user_id)
                    VALUES
                    (:group_id, :user_id)
                    """,
                    {
                        "group_id": group_id,
                        "user_id": user[0]
                    }
                )

                conn.commit()

                messagebox.showinfo(
                    "Success",
                    "Member added successfully."
                )

                member_window.destroy()

            except Exception as e:

                conn.rollback()

                messagebox.showerror(
                    "Error",
                    str(e)
                )

            finally:

                cursor.close()
                conn.close()

        tk.Button(
            member_window,
            text="Add Member",
            command=save_member
        ).pack(pady=20)