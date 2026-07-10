import tkinter as tk
from tkinter import messagebox
from tkcalendar import Calendar


class CalendarView:
    def __init__(self, app):
        self.app = app

        tk.Label(
            app.container,
            text="日付選択",
            font=("Arial", 24, "bold")
        ).pack(pady=20)

        tk.Label(
            app.container,
            text="日付を選択してください。",
            font=("Arial", 14)
        ).pack()

        # date_patternを明示することで、ロケールによってget_date()の
        # 書式が変わるのを防ぐ。ここを変える場合は
        # position_edit_view.pyのchange_date()も合わせて直すこと。
        self.calendar = Calendar(app.container, date_pattern="yyyy-mm-dd")
        self.calendar.pack(pady=20)

        tk.Button(
            app.container,
            text="この日付で開始",
            command=self.select_date
        ).pack(pady=20)

    def select_date(self):
        date = self.calendar.get_date()

        if not date:
            messagebox.showerror("エラー", "日付を選択してください")
            return

        self.app.selected_date = date
        self.app.show_crew_list_view()