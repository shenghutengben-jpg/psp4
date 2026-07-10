import tkinter as tk
from views import (
    CalendarView,
    CrewListView,
    CrewFormView,
    TimeSlotView,
    PositionEditView
)


class PositioningApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("ポジショニング管理システム")
        self.geometry("1200x800")

        # ウィンドウサイズを固定し、最大化・リサイズを禁止する。
        # pack()は中身のサイズにぴったり合わせて配置されるため、
        # ウィンドウだけを大きくすると中身とのバランスが崩れて見える。
        # 各画面をリサイズ対応にするのは工数がかかるため、
        # 今回は「テスト済みの見た目のまま固定する」方針で対応する。
        self.resizable(False, False)

        self.selected_date = None
        self.selected_time_slot = None
        self.position_assignments = {}

        self.time_slots = [f"{i:02}:00〜{i+1:02}:00" for i in range(24)]
        self.current_time_slot_index = None

        self.dummy_crews = [
            {"name": "Aさん", "start": "11:00", "end": "18:00"},
            {"name": "Bさん", "start": "16:00", "end": "24:00"},
            {"name": "Cさん", "start": "14:00", "end": "23:00"},
            {"name": "Dさん", "start": "17:00", "end": "21:00"},
        ]

        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)

        self.show_calendar_view()

    def clear_screen(self):
        for widget in self.container.winfo_children():
            widget.destroy()

    def show_calendar_view(self):
        self.clear_screen()
        CalendarView(self)

    def show_crew_list_view(self):
        self.clear_screen()
        CrewListView(self)

    def show_crew_form_view(self):
        self.clear_screen()
        CrewFormView(self)

    def show_time_slot_view(self):
        self.clear_screen()
        TimeSlotView(self)

    def show_position_edit_view(self):
        self.clear_screen()
        PositionEditView(self)


def main():
    app = PositioningApp()
    app.mainloop()


if __name__ == "__main__":
    main()