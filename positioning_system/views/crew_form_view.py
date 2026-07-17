import tkinter as tk
from tkinter import ttk, messagebox

from controllers.date_controller import add_schedule_by_crew_name


class CrewFormView(tk.Frame):
    def __init__(self, master, get_selected_date, on_next, on_back):
        super().__init__(master)

        self.get_selected_date = get_selected_date
        self.on_next = on_next
        self.on_back = on_back

        self.time_options = self.create_time_options()

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

        tk.Label(self, text="出勤時間").pack()
        self.start_combo = ttk.Combobox(
            self,
            values=self.time_options,
            state="readonly",
            width=27
        )
        self.start_combo.pack(pady=5)

        tk.Label(self, text="退勤時間").pack()
        self.end_combo = ttk.Combobox(
            self,
            values=self.time_options,
            state="readonly",
            width=27
        )
        self.end_combo.pack(pady=5)

        # 初期値
        self.start_combo.set("09:00")
        self.end_combo.set("18:00")

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

    def create_time_options(self):
        """
        00:00〜24:00 までの時間選択肢を作る。
        30分刻み。
        """

        options = []

        for hour in range(24):
            options.append(f"{hour:02d}:00")

        options.append("24:00")

        return options

    def register_schedule(self):
        date = self.get_selected_date()
        crew_name = self.name_entry.get().strip()
        start_time = self.start_combo.get()
        end_time = self.end_combo.get()

        if not date:
            messagebox.showerror("エラー", "日付が選択されていません")
            return

        if not crew_name:
            messagebox.showerror("エラー", "クルー名を入力してください")
            return

        if not start_time or not end_time:
            messagebox.showerror("エラー", "出勤時間と退勤時間を選択してください")
            return

        try:
            add_schedule_by_crew_name(
                date=date,
                crew_name=crew_name,
                start_time=start_time,
                end_time=end_time
            )

        except ValueError as e:
            messagebox.showerror("入力エラー", str(e))
            return

        messagebox.showinfo(
            "登録完了",
            f"{crew_name} の勤務を登録しました"
        )

        self.name_entry.delete(0, tk.END)
        self.start_combo.set("09:00")
        self.end_combo.set("18:00")