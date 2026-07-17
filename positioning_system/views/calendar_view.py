import tkinter as tk
from tkcalendar import Calendar


class CalendarView(tk.Frame):
    def __init__(self, master, on_date_selected):
        super().__init__(master)

        self.on_date_selected = on_date_selected

        tk.Label(
            self,
            text="日付選択画面",
            font=("Arial", 18)
        ).pack(pady=20)

        self.calendar = Calendar(
            self,
            selectmode="day",
            date_pattern="yyyy-mm-dd"
        )
        self.calendar.pack(pady=20)

        tk.Button(
            self,
            text="この日付を選択して次へ",
            command=self.select_date
        ).pack(pady=10)

    def select_date(self):
        selected_date = self.calendar.get_date()
        self.on_date_selected(selected_date)