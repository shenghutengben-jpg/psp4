import tkinter as tk

from views.calendar_view import CalendarView
from views.crew_form_view import CrewFormView
from views.crew_list_view import CrewListView


class DebugApp:
    def __init__(self, root):
        self.root = root
        self.current_frame = None

        self.selected_date = None

        self.show_calendar_view()

    def clear_frame(self):
        if self.current_frame is not None:
            self.current_frame.destroy()

    def show_calendar_view(self):
        self.clear_frame()

        self.current_frame = CalendarView(
            self.root,
            on_date_selected=self.set_date
        )
        self.current_frame.pack(fill=tk.BOTH, expand=True)

    def show_crew_form_view(self):
        self.clear_frame()

        self.current_frame = CrewFormView(
            self.root,
            get_selected_date=self.get_selected_date,
            on_next=self.show_crew_list_view,
            on_back=self.show_calendar_view
        )
        self.current_frame.pack(fill=tk.BOTH, expand=True)

    def show_crew_list_view(self):
        self.clear_frame()

        self.current_frame = CrewListView(
            self.root,
            get_selected_date=self.get_selected_date,
            on_next=self.debug_next,
            on_back=self.show_crew_form_view
        )
        self.current_frame.pack(fill=tk.BOTH, expand=True)

    def set_date(self, date):
        self.selected_date = date
        print("選択された日付:", self.selected_date)
        self.show_crew_form_view()

    def get_selected_date(self):
        return self.selected_date

    def debug_next(self):
        print("crew_list_view まで確認できました")


def main():
    root = tk.Tk()
    root.title("crew_listまでのデバッグ")
    root.geometry("800x600")

    DebugApp(root)

    root.mainloop()


if __name__ == "__main__":
    main()