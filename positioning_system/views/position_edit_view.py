import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta


class PositionEditView:
    def __init__(self, app):
        self.app = app

        # この時間帯専用の配置情報を取り出す（無ければ空のdictを新規作成）。
        # setdefaultで取り出したdictはapp.position_assignments内の実体への
        # 参照なので、ここでの変更はそのままapp側にも反映される。
        self.slot_assignments = self.app.position_assignments.setdefault(
            self.app.selected_time_slot, {}
        )

        self.available_crews = self.filter_active_crews()

        # すでにこの時間帯で配置済みのクルーは、クルー一覧側から除外しておく
        for crew in self.slot_assignments.values():
            if crew in self.available_crews:
                self.available_crews.remove(crew)

        tk.Label(
            app.container,
            text="ポジション編集",
            font=("Arial", 22, "bold")
        ).pack(pady=10)

        tk.Label(
            app.container,
            text="クルーをドラッグしてポジションへドロップしてください。"
                 "配置済みのクルーも同様にドラッグして移動・解除できます。",
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
        # ドラッグの開始元。ポジションから始めた場合はそのポジション名、
        # クルー一覧から始めた場合はNone。
        self.drag_source_position = None

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

            # ポジションに配置済みのクルーも再度ドラッグできるようにする。
            # start_position_dragは、そのポジションが空の場合は何もしない。
            label.bind("<Button-1>",
                       lambda e, p=position: self.start_position_drag(e, p))
            label.bind("<B1-Motion>", self.drag_motion)
            label.bind("<ButtonRelease-1>", self.drop_crew)

            self.position_labels[position] = label

            # 前回この時間帯を編集したときの配置が残っていれば表示を復元する
            if position in self.slot_assignments:
                crew = self.slot_assignments[position]
                label.config(text=f"{position}：{crew['name']}")

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
        slot_start, slot_end = self.app.selected_time_slot.split("〜")

        active_crews = []

        for crew in self.app.dummy_crews:
            # クルーの勤務時間[start, end)と時間帯[slot_start, slot_end)が
            # 重なっていれば「その時間帯に出勤している」とみなす。
            if crew["start"] < slot_end and crew["end"] > slot_start:
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

    def start_drag(self, event, crew, source_position=None):
        self.dragging_crew = crew
        self.drag_source_position = source_position

        self.drag_label = tk.Label(
            self.app.container,
            text=crew["name"],
            bg="yellow",
            relief="solid"
        )

        x = event.x_root - self.app.winfo_rootx()
        y = event.y_root - self.app.winfo_rooty()

        self.drag_label.place(x=x, y=y)

    def start_position_drag(self, event, position):
        # そのポジションに誰も配置されていなければドラッグを開始しない
        crew = self.slot_assignments.get(position)
        if not crew:
            return

        self.start_drag(event, crew, source_position=position)

    def drag_motion(self, event):
        if self.drag_label:
            x = event.x_root - self.app.winfo_rootx()
            y = event.y_root - self.app.winfo_rooty()

            self.drag_label.place(x=x + 5, y=y + 5)

    def drop_crew(self, event):
        if not self.dragging_crew:
            return

        crew = self.dragging_crew
        source_position = self.drag_source_position

        dropped_position = None

        for position, label in self.position_labels.items():
            x1 = label.winfo_rootx()
            y1 = label.winfo_rooty()
            x2 = x1 + label.winfo_width()
            y2 = y1 + label.winfo_height()

            if x1 <= event.x_root <= x2 and y1 <= event.y_root <= y2:
                dropped_position = position
                break

        if dropped_position and dropped_position != source_position:
            # 移動先に既に別のクルーがいる場合は、そのクルーをクルー一覧へ戻す
            previous_crew = self.slot_assignments.get(dropped_position)
            if previous_crew and previous_crew is not crew:
                self.available_crews.append(previous_crew)

            # ポジションからポジションへの移動の場合、移動元を空にする
            if source_position:
                self.slot_assignments.pop(source_position, None)
                self.position_labels[source_position].config(text=source_position)

            self.slot_assignments[dropped_position] = crew
            self.position_labels[dropped_position].config(
                text=f"{dropped_position}：{crew['name']}"
            )

            if crew in self.available_crews:
                self.available_crews.remove(crew)

            self.refresh_crews()

        elif dropped_position is None and source_position:
            # ポジション以外の場所へドロップした場合は配置を解除し、
            # クルーを一覧へ戻す
            self.slot_assignments.pop(source_position, None)
            self.position_labels[source_position].config(text=source_position)

            if crew not in self.available_crews:
                self.available_crews.append(crew)

            self.refresh_crews()

        # dropped_position == source_position（同じ場所に戻した場合）や、
        # クルー一覧からドラッグしてポジション以外へ落とした場合は
        # 何も変更しない

        if self.drag_label:
            self.drag_label.destroy()

        self.drag_label = None
        self.dragging_crew = None
        self.drag_source_position = None

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
            "%Y-%m-%d"
        )

        new_date = current_date + timedelta(days=days)

        self.app.selected_date = new_date.strftime("%Y-%m-%d")