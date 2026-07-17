import tkinter as tk

from views.calendar_view import CalendarView


def on_date_selected(date):
    print("選択された日付:", date)


def main():
    root = tk.Tk()
    root.title("カレンダー画面デバッグ")
    root.geometry("500x400")

    calendar_view = CalendarView(
        root,
        on_date_selected=on_date_selected
    )
    calendar_view.pack(fill=tk.BOTH, expand=True)

    root.mainloop()


if __name__ == "__main__":
    main()