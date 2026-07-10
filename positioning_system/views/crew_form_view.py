import tkinter as tk
from tkinter import messagebox
import re


TIME_PATTERN = re.compile(r"^\d{2}:\d{2}$")


def is_valid_time(time_str):
    """HH:MM形式かつ実在する時刻かどうかを判定する。
    "24:00" は「日をまたいで退勤する」ことを表す特別な値として許可する。
    """
    if not TIME_PATTERN.match(time_str):
        return False

    hour, minute = map(int, time_str.split(":"))

    if minute > 59:
        return False

    if hour == 24:
        return minute == 0

    return 0 <= hour <= 23


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

        tk.Label(app.container, text="クルー名").pack()
        self.name_entry = tk.Entry(app.container)
        self.name_entry.pack(pady=5)

        tk.Label(app.container, text="出勤時間（例: 09:00）").pack()
        self.start_entry = tk.Entry(app.container)
        self.start_entry.pack(pady=5)

        tk.Label(app.container, text="退勤時間（例: 18:00）").pack()
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
        name = self.name_entry.get().strip()
        start = self.start_entry.get().strip()
        end = self.end_entry.get().strip()

        if not name:
            messagebox.showerror("入力エラー", "クルー名を入力してください")
            return

        if not is_valid_time(start) or not is_valid_time(end):
            messagebox.showerror(
                "入力エラー",
                "出勤時間・退勤時間は HH:MM 形式（00:00〜24:00）で入力してください"
            )
            return

        if start >= end:
            messagebox.showerror(
                "入力エラー",
                "退勤時間は出勤時間より後の時刻にしてください"
            )
            return

        self.app.dummy_crews.append({
            "name": name,
            "start": start,
            "end": end
        })

        self.app.show_crew_list_view()