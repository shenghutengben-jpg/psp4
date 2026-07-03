import tkinter as tk


class TimeSlotView:
    def __init__(self, app):
        self.app = app

        tk.Label(
            app.container,
            text="時間帯選択",
            font=("Arial", 22, "bold")
        ).pack(pady=20)

        tk.Label(
            app.container,
            text="ポジショニングを行う時間帯を選択してください。",
            font=("Arial", 12)
        ).pack()

        frame = tk.Frame(app.container)
        frame.pack()

        for index, slot in enumerate(app.time_slots):
            row = index // 3
            col = index % 3

            tk.Button(
                frame,
                text=slot,
                width=18,
                command=lambda i=index: self.select_time_slot(i)
            ).grid(row=row, column=col, padx=5, pady=5)

        tk.Button(
            app.container,
            text="戻る",
            command=app.show_crew_list_view
        ).pack(pady=20)

    def select_time_slot(self, index):
        self.app.current_time_slot_index = index
        self.app.selected_time_slot = self.app.time_slots[index]
        self.app.show_position_edit_view()