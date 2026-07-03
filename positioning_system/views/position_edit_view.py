import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta


class PositionEditView:
    def __init__(self, app):
        self.app = app
        self.available_crews = self.filter_active_crews()

        tk.Label(
            app.container,
            text="ポジション編集",
            font=("Arial", 22, "bold")
        ).pack(pady=10)

        tk.Label(
            app.container,
            text="登録されているクルーの一覧からクルーをドラッグし、ポジションへドロップしてください。",
            font=("Arial", 12)
        ).pack()

        top_frame = tk.Frame(app.container)
        top_frame.pack(fill="x")

        tk.Button(
            top_frame,
            text="前の時間帯を編集する",
            command=self.prev_slot
        ).pack(side="left", padx=10)

        tk.Button(
            top_frame,
            text="次の時間帯を編集する",
            command=self.next_slot
        ).pack(side="right", padx=10)

        tk.Label(
            app.container,
            text=f"{app.selected_date} / {app.selected_time_slot}"
        ).pack(pady=10)

        self.position_labels = {}
        self.drag_label = None
        self.dragging_crew = None

        main_frame = tk.Frame(app.container)
        main_frame.pack()

        self.crew_frame = tk.LabelFrame(main_frame, text="クルー")
        self.crew_frame.grid(row=0, column=0, padx=20)

        position_frame = tk.LabelFrame(main_frame, text="ポジション")
        position_frame.grid(row=0, column=1, padx=20)

        self.positions = [
            "イニシ",
            "カウンター",
            "スルー",
            "ストッカー",
            "厨房",
            "休憩"
        ]

        self.refresh_crews()

        for position in self.positions:
            label = tk.Label(
                position_frame,
                text=position,
                relief="solid",
                width=25,
                height=2
            )
            label.pack(pady=5)

            self.position_labels[position] = label

        tk.Button(
            app.container,
            text="保存",
            command=self.save_assignments
        ).pack(pady=10)

        tk.Button(
            app.container,
            text="時間帯選択へ戻る",
            command=app.show_time_slot_view
        ).pack()

    def filter_active_crews(self):
        current_start = self.app.selected_time_slot.split("〜")[0]

        active_crews = []

        for crew in self.app.dummy_crews:
            if crew["end"] > current_start:
                active_crews.append(crew)

        return active_crews

    def refresh_crews(self):
        for widget in self.crew_frame.winfo_children():
            widget.destroy()

        for crew in self.available_crews:
            label = tk.Label(
                self.crew_frame,
                text=crew["name"],
                relief="solid",
                width=20
            )
            label.pack(pady=5)

            label.bind("<Button-1>",
                       lambda e, c=crew: self.start_drag(e, c))
            label.bind("<B1-Motion>", self.drag_motion)
            label.bind("<ButtonRelease-1>", self.drop_crew)

    def start_drag(self, event, crew):
        self.dragging_crew = crew

        self.drag_label = tk.Label(
            self.app.container,
            text=crew["name"],
            bg="yellow",
            relief="solid"
        )

        x = event.x_root - self.app.winfo_rootx()
        y = event.y_root - self.app.winfo_rooty()

        self.drag_label.place(x=x, y=y)

    def drag_motion(self, event):
        if self.drag_label:
            x = event.x_root - self.app.winfo_rootx()
            y = event.y_root - self.app.winfo_rooty()

            self.drag_label.place(x=x + 5, y=y + 5)

    def drop_crew(self, event):
        if not self.dragging_crew:
            return

        dropped_position = None

        for position, label in self.position_labels.items():
            x1 = label.winfo_rootx()
            y1 = label.winfo_rooty()
            x2 = x1 + label.winfo_width()
            y2 = y1 + label.winfo_height()

            if x1 <= event.x_root <= x2 and y1 <= event.y_root <= y2:
                dropped_position = position
                break

        if dropped_position:
            crew = self.dragging_crew

            self.app.position_assignments[dropped_position] = crew

            self.position_labels[dropped_position].config(
                text=f"{dropped_position}：{crew['name']}"
            )

            if crew in self.available_crews:
                self.available_crews.remove(crew)

            self.refresh_crews()

        if self.drag_label:
            self.drag_label.destroy()

        self.drag_label = None
        self.dragging_crew = None

    def save_assignments(self):
        messagebox.showinfo("保存", "配置情報を保存しました")

    def prev_slot(self):
        if self.app.current_time_slot_index > 0:
            self.app.current_time_slot_index -= 1
        else:
            self.app.current_time_slot_index = 23
            self.change_date(-1)

        self.app.selected_time_slot = self.app.time_slots[
            self.app.current_time_slot_index
        ]
        self.app.show_position_edit_view()

    def next_slot(self):
        if self.app.current_time_slot_index < 23:
            self.app.current_time_slot_index += 1
        else:
            self.app.current_time_slot_index = 0
            self.change_date(1)

        self.app.selected_time_slot = self.app.time_slots[
            self.app.current_time_slot_index
        ]
        self.app.show_position_edit_view()

    def change_date(self, days):
        current_date = datetime.strptime(
            self.app.selected_date,
            "%m/%d/%y"
        )

        new_date = current_date + timedelta(days=days)

        self.app.selected_date = new_date.strftime("%m/%d/%y")