"""
クルー勤務一覧画面。

指定した日付に登録されている勤務予定(Schedule)の一覧を表示する。
"""

import tkinter as tk
from tkinter import ttk, messagebox

<<<<<<< HEAD
from controllers import get_schedules_by_date, get_crew_by_id
=======
from controllers.date_controller import get_schedules_by_date
from controllers.crew_controller import get_crew_by_id
>>>>>>> main


class CrewListView(tk.Frame):
    def __init__(self, master, get_selected_date, on_next, on_back):
        super().__init__(master)
<<<<<<< HEAD

        self.get_selected_date = get_selected_date
        self.on_next = on_next
        self.on_back = on_back

        tk.Label(self, text="クルー勤務一覧画面", font=("Arial", 18)).pack(pady=20)

        self.date_label = tk.Label(
            self, text=f"選択日: {self.get_selected_date()}"
        )
        self.date_label.pack(pady=5)

        self.tree = ttk.Treeview(
            self,
            columns=("crew_name", "start_time", "end_time"),
            show="headings",
            height=12
        )
        self.tree.heading("crew_name", text="クルー名")
        self.tree.heading("start_time", text="出勤時間")
        self.tree.heading("end_time", text="退勤時間")
        self.tree.column("crew_name", width=180)
        self.tree.column("start_time", width=120)
        self.tree.column("end_time", width=120)
=======

        self.get_selected_date = get_selected_date
        self.on_next = on_next
        self.on_back = on_back

        tk.Label(
            self,
            text="クルー勤務一覧画面",
            font=("Arial", 18)
        ).pack(pady=20)

        self.date_label = tk.Label(
            self,
            text=f"選択日: {self.get_selected_date()}"
        )
        self.date_label.pack(pady=5)

        self.tree = ttk.Treeview(
            self,
            columns=("crew_name", "start_time", "end_time"),
            show="headings",
            height=12
        )

        self.tree.heading("crew_name", text="クルー名")
        self.tree.heading("start_time", text="出勤時間")
        self.tree.heading("end_time", text="退勤時間")

        self.tree.column("crew_name", width=180)
        self.tree.column("start_time", width=120)
        self.tree.column("end_time", width=120)

>>>>>>> main
        self.tree.pack(pady=10)

        button_frame = tk.Frame(self)
        button_frame.pack(pady=10)

        tk.Button(
<<<<<<< HEAD
            button_frame, text="一覧更新", command=self.refresh
        ).grid(row=0, column=0, padx=5)

        tk.Button(
            button_frame, text="勤務登録へ戻る", command=self.on_back
        ).grid(row=0, column=1, padx=5)

        tk.Button(
            button_frame, text="時間帯選択へ", command=self.on_next
        ).grid(row=0, column=2, padx=5)

=======
            button_frame,
            text="一覧更新",
            command=self.refresh
        ).grid(row=0, column=0, padx=5)

        tk.Button(
            button_frame,
            text="勤務登録へ戻る",
            command=self.on_back
        ).grid(row=0, column=1, padx=5)

        tk.Button(
            button_frame,
            text="時間帯選択へ",
            command=self.on_next
        ).grid(row=0, column=2, padx=5)

>>>>>>> main
        self.refresh()

    def refresh(self):
        date = self.get_selected_date()

        if not date:
            messagebox.showerror("エラー", "日付が選択されていません")
            return

        self.date_label.config(text=f"選択日: {date}")

        for item in self.tree.get_children():
            self.tree.delete(item)

        schedules = get_schedules_by_date(date)

        for schedule in schedules:
<<<<<<< HEAD
            crew = get_crew_by_id(schedule.crew_id)
            crew_name = crew.name if crew is not None else "不明なクルー"
=======
            crew = get_crew_by_id(schedule["crew_id"])

            if crew is None:
                crew_name = "不明なクルー"
            else:
                crew_name = crew["name"]
>>>>>>> main

            self.tree.insert(
                "",
                tk.END,
<<<<<<< HEAD
                values=(crew_name, schedule.start_time, schedule.end_time)
=======
                values=(
                    crew_name,
                    schedule["start_time"],
                    schedule["end_time"]
                )
>>>>>>> main
            )