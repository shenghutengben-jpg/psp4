import tkinter as tk


class CrewListView:
    def __init__(self, app):
        self.app = app

        tk.Label(
            app.container,
            text="クルー一覧",
            font=("Arial", 22, "bold")
        ).pack(pady=20)

        tk.Label(
            app.container,
            text=f"選択日：{app.selected_date}",
            font=("Arial", 14)
        ).pack()

        for crew in app.dummy_crews:
            tk.Label(
                app.container,
                text=f'{crew["name"]} {crew["start"]}〜{crew["end"]}'
            ).pack()

        button_frame = tk.Frame(app.container)
        button_frame.pack(pady=20)

        tk.Button(
            button_frame,
            text="クルーを追加する",
            command=app.show_crew_form_view
        ).grid(row=0, column=0, padx=10)

        tk.Button(
            button_frame,
            text="時間帯選択へ",
            command=app.show_time_slot_view
        ).grid(row=0, column=1, padx=10)

        tk.Button(
            button_frame,
            text="戻る",
            command=app.show_calendar_view
        ).grid(row=0, column=2, padx=10)