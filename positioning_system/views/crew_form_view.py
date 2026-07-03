import tkinter as tk
from tkinter import messagebox
import re


class CrewFormView:
    def __init__(self, app):
        self.app = app

        tk.Label(
            app.container,
            text="クルー登録",
            font=("Arial", 22, "bold")
        ).pack(pady=20)

        tk.Label(
            app.container,
            text="追加するクルーの情報を入力してください。",
            font=("Arial", 12)
        ).pack()

        self.name_entry = tk.Entry(app.container)
        self.name_entry.pack(pady=5)

        self.start_entry = tk.Entry(app.container)
        self.start_entry.pack(pady=5)

        self.end_entry = tk.Entry(app.container)
        self.end_entry.pack(pady=5)

        tk.Button(
            app.container,
            text="登録する",
            command=self.register
        ).pack(pady=20)

        tk.Button(
            app.container,
            text="戻る",
            command=app.show_crew_list_view
        ).pack()

    def register(self):
        name = self.name_entry.get()
        start = self.start_entry.get()
        end = self.end_entry.get()

        pattern = r"^\d{2}:\d{2}$"

        if not re.match(pattern, start) or not re.match(pattern, end):
            messagebox.showerror(
                "入力エラー",
                "出勤時間・退勤時間は HH:MM 形式で入力してください"
            )
            return

        self.app.dummy_crews.append({
            "name": name,
            "start": start,
            "end": end
        })

        self.app.show_crew_list_view()