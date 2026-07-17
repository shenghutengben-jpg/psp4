import tkinter as tk
from tkinter import messagebox

from controllers.date_controller import add_schedule_by_crew_name


class CrewFormView(tk.Frame):
    def __init__(self, master, get_selected_date, on_next, on_back):
        super().__init__(master)

        self.get_selected_date = get_selected_date
        self.on_next = on_next
        self.on_back = on_back

        tk.Label(
            self,
            text="クルー勤務登録画面",
            font=("Arial", 18)
        ).pack(pady=20)

        self.date_label = tk.Label(
            self,
            text=f"選択日: {self.get_selected_date()}"
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
            self,
            text="勤務登録",
            command=self.register_schedule
        ).pack(pady=10)

        tk.Button(
            self,
            text="登録済みクルー一覧へ",
            command=self.on_next
        ).pack(pady=5)

        tk.Button(
            self,
            text="日付選択へ戻る",
            command=self.on_back
        ).pack(pady=5)

    def register_schedule(self):
        date = self.get_selected_date()
        crew_name = self.name_entry.get().strip()
        start_time = self.start_entry.get().strip()
        end_time = self.end_entry.get().strip()

        if not date:
            messagebox.showerror("エラー", "日付が選択されていません")
            return

        if not crew_name or not start_time or not end_time:
            messagebox.showerror("エラー", "未入力の項目があります")
            return

        add_schedule_by_crew_name(
            date=date,
            crew_name=crew_name,
            start_time=start_time,
            end_time=end_time
        )

        messagebox.showinfo(
            "登録完了",
            f"{crew_name} の勤務を登録しました"
        )

        self.name_entry.delete(0, tk.END)
        self.start_entry.delete(0, tk.END)
        self.end_entry.delete(0, tk.END)