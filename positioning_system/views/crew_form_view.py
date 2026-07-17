"""
クルー勤務登録画面。

指定した日付に対して、クルー名・出勤時間・退勤時間を入力し、
Schedule（勤務予定）として登録する画面。
クルー名が未登録であれば自動的にクルーマスタへ新規登録される
（controllers.get_or_create_crew を参照）。
"""

import tkinter as tk
from tkinter import messagebox

from controllers import add_schedule_by_crew_name


def is_valid_time(time_str: str) -> bool:
    """
    "HH:MM" 形式かつ実在する時刻かどうかを判定する。
    "24:00" は「日をまたいで退勤する」ことを表す特別な値として許可する。
    """
    parts = time_str.split(":")
    if len(parts) != 2:
        return False

    hour_str, minute_str = parts
    if not (hour_str.isdigit() and minute_str.isdigit()):
        return False
    if len(hour_str) != 2 or len(minute_str) != 2:
        return False

    hour, minute = int(hour_str), int(minute_str)

    if minute > 59:
        return False
    if hour == 24:
        return minute == 0
    return 0 <= hour <= 23


class CrewFormView(tk.Frame):
    def __init__(self, master, get_selected_date, on_next, on_back):
        super().__init__(master)

        self.get_selected_date = get_selected_date
        self.on_next = on_next
        self.on_back = on_back

        tk.Label(self, text="クルー勤務登録画面", font=("Arial", 18)).pack(pady=20)

        self.date_label = tk.Label(
            self, text=f"選択日: {self.get_selected_date()}"
        )
        self.date_label.pack(pady=5)

        tk.Label(self, text="クルー名").pack()
        self.name_entry = tk.Entry(self, width=30)
        self.name_entry.pack(pady=5)

        tk.Label(self, text="出勤時間 例: 12:00").pack()
        self.start_entry = tk.Entry(self, width=30)
        self.start_entry.pack(pady=5)

        tk.Label(self, text="退勤時間 例: 18:00").pack()
        self.end_entry = tk.Entry(self, width=30)
        self.end_entry.pack(pady=5)

        tk.Button(
            self, text="勤務登録", command=self.register_schedule
        ).pack(pady=10)

        tk.Button(
            self, text="登録済みクルー一覧へ", command=self.on_next
        ).pack(pady=5)

        tk.Button(
            self, text="日付選択へ戻る", command=self.on_back
        ).pack(pady=5)

    def register_schedule(self):
        date = self.get_selected_date()
        crew_name = self.name_entry.get().strip()
        start_time = self.start_entry.get().strip()
        end_time = self.end_entry.get().strip()

        if not date:
            messagebox.showerror("エラー", "日付が選択されていません")
            return

        if not crew_name:
            messagebox.showerror("エラー", "クルー名を入力してください")
            return

        if not is_valid_time(start_time) or not is_valid_time(end_time):
            messagebox.showerror(
                "エラー",
                "出勤時間・退勤時間は HH:MM 形式（00:00〜24:00）で入力してください"
            )
            return

        if start_time >= end_time:
            messagebox.showerror(
                "エラー", "退勤時間は出勤時間より後の時刻にしてください"
            )
            return

        add_schedule_by_crew_name(
            date=date,
            crew_name=crew_name,
            start_time=start_time,
            end_time=end_time,
        )

        messagebox.showinfo("登録完了", f"{crew_name} の勤務を登録しました")

        self.name_entry.delete(0, tk.END)
        self.start_entry.delete(0, tk.END)
        self.end_entry.delete(0, tk.END)