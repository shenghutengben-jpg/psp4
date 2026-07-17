"""
ポジション編集画面。

指定した日付・時間帯において、出勤しているクルーをポジションへ
ドラッグ＆ドロップで配置する画面。

【保存タイミングについての設計判断】
仕様書 4.8(ポジショニング保存機能)には「利用者は『保存』ボタンを
押すことで、現在のポジショニング情報を保存できる」と明記されている。
そのため、ドラッグ＆ドロップの時点では変更をこの画面内のメモリ上
(self.slot_assignments)にのみ保持し、実際にJSONファイルへ書き込む
(controllers.assign_crew_to_position等を呼び出す)のは「保存」ボタンが
押された時だけにしている。
こうすることで、ドラッグのたびにファイルへ読み書きするのを避けられ、
仕様書のユースケース「前後の時間帯へ移動する」の例外フロー
(2e. 保存されていない変更が存在する場合、保存確認ダイアログを表示する)
も自然に実装できる。
"""

import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta

from controllers import (
    get_working_crews,
    get_time_slot_by_id,
    get_previous_time_slot,
    get_next_time_slot,
    get_all_time_slots,
    get_all_positions,
    get_assignments_by_date_and_time_slot,
    assign_crew_to_position,
    delete_assignment,
    AssignmentConflictError,
    get_crew_by_id,
)


class PositionEditView(tk.Frame):
    def __init__(
        self,
        master,
        get_selected_date,
        get_selected_time_slot_id,
        on_navigate,
        on_back,
    ):
        super().__init__(master)

        self.get_selected_date = get_selected_date
        self.get_selected_time_slot_id = get_selected_time_slot_id
        self.on_navigate = on_navigate
        self.on_back = on_back

        self.date = self.get_selected_date()
        self.time_slot_id = self.get_selected_time_slot_id()
        self.time_slot = get_time_slot_by_id(self.time_slot_id)

        self.positions = get_all_positions()
        self.positions_by_id = {p.id: p for p in self.positions}

        # この時間帯に出勤しているクルー一覧（編集対象の母集団）
        working_crews = get_working_crews(self.date, self.time_slot_id)

        # すでに保存されている配置情報を読み込み、
        # {position_id: Crew} の下書き(draft)として保持する。
        # このdraftを直接編集し、「保存」が押された時だけ
        # controllers経由でJSONへ反映する。
        initial_assignments = get_assignments_by_date_and_time_slot(
            self.date, self.time_slot_id
        )
        self.slot_assignments = {}
        for assignment in initial_assignments:
            crew = get_crew_by_id(assignment.crew_id)
            if crew is not None:
                self.slot_assignments[assignment.position_id] = crew

        # 「保存」を押した時点の状態と比較するための基準値。
        # 保存に成功するたびに更新する。
        self.initial_position_crew_ids = {
            position_id: crew.id
            for position_id, crew in self.slot_assignments.items()
        }

        # クルー一覧側に表示する「まだどこにも配置されていないクルー」
        assigned_crew_ids = {c.id for c in self.slot_assignments.values()}
        self.available_crews = [
            c for c in working_crews if c.id not in assigned_crew_ids
        ]

        tk.Label(
            self, text="ポジション編集", font=("Arial", 22, "bold")
        ).pack(pady=10)

        tk.Label(
            self,
            text="クルーをドラッグしてポジションへドロップしてください。"
                 "配置済みのクルーも同様にドラッグして移動・解除できます。",
            font=("Arial", 12)
        ).pack()

        top_frame = tk.Frame(self)
        top_frame.pack(fill="x")

        tk.Button(
            top_frame, text="前の時間帯を編集する", command=self.prev_slot
        ).pack(side="left", padx=10)

        tk.Button(
            top_frame, text="次の時間帯を編集する", command=self.next_slot
        ).pack(side="right", padx=10)

        slot_label = (
            f"{self.time_slot.start_time}〜{self.time_slot.end_time}"
            if self.time_slot is not None
            else "（時間帯不明）"
        )
        tk.Label(self, text=f"{self.date} / {slot_label}").pack(pady=10)

        self.position_labels = {}
        self.drag_label = None
        self.dragging_crew = None
        self.drag_source_position_id = None

        main_frame = tk.Frame(self)
        main_frame.pack()

        self.crew_frame = tk.LabelFrame(main_frame, text="クルー")
        self.crew_frame.grid(row=0, column=0, padx=20)

        position_frame = tk.LabelFrame(main_frame, text="ポジション")
        position_frame.grid(row=0, column=1, padx=20)

        self.refresh_crews()

        if not self.positions:
            tk.Label(
                position_frame, text="ポジションが登録されていません", fg="red"
            ).pack(pady=10)

        for position in self.positions:
            label = tk.Label(
                position_frame,
                text=position.name,
                relief="solid",
                width=25,
                height=2
            )
            label.pack(pady=5)

            label.bind(
                "<Button-1>",
                lambda e, p=position: self.start_position_drag(e, p)
            )
            label.bind("<B1-Motion>", self.drag_motion)
            label.bind("<ButtonRelease-1>", self.drop_crew)

            self.position_labels[position.id] = label

            if position.id in self.slot_assignments:
                crew = self.slot_assignments[position.id]
                label.config(text=f"{position.name}：{crew.name}")

        tk.Button(
            self, text="保存", command=self.save_assignments
        ).pack(pady=10)

        tk.Button(
            self, text="時間帯選択へ戻る", command=self.handle_back
        ).pack()

    # --- ドラッグ＆ドロップまわり ---

    def refresh_crews(self):
        for widget in self.crew_frame.winfo_children():
            widget.destroy()

        for crew in self.available_crews:
            label = tk.Label(
                self.crew_frame, text=crew.name, relief="solid", width=20
            )
            label.pack(pady=5)

            label.bind("<Button-1>", lambda e, c=crew: self.start_drag(e, c))
            label.bind("<B1-Motion>", self.drag_motion)
            label.bind("<ButtonRelease-1>", self.drop_crew)

    def start_drag(self, event, crew, source_position_id=None):
        self.dragging_crew = crew
        self.drag_source_position_id = source_position_id

        self.drag_label = tk.Label(
            self, text=crew.name, bg="yellow", relief="solid"
        )

        x = event.x_root - self.winfo_rootx()
        y = event.y_root - self.winfo_rooty()
        self.drag_label.place(x=x, y=y)

    def start_position_drag(self, event, position):
        crew = self.slot_assignments.get(position.id)
        if crew is None:
            return
        self.start_drag(event, crew, source_position_id=position.id)

    def drag_motion(self, event):
        if self.drag_label:
            x = event.x_root - self.winfo_rootx()
            y = event.y_root - self.winfo_rooty()
            self.drag_label.place(x=x + 5, y=y + 5)

    def drop_crew(self, event):
        if not self.dragging_crew:
            return

        crew = self.dragging_crew
        source_position_id = self.drag_source_position_id

        dropped_position_id = None
        for position_id, label in self.position_labels.items():
            x1 = label.winfo_rootx()
            y1 = label.winfo_rooty()
            x2 = x1 + label.winfo_width()
            y2 = y1 + label.winfo_height()

            if x1 <= event.x_root <= x2 and y1 <= event.y_root <= y2:
                dropped_position_id = position_id
                break

        if dropped_position_id is not None and dropped_position_id != source_position_id:
            # 移動先に既に別のクルーがいる場合は、クルー一覧へ戻す
            previous_crew = self.slot_assignments.get(dropped_position_id)
            if previous_crew is not None and previous_crew.id != crew.id:
                self.available_crews.append(previous_crew)

            # 元がポジションからのドラッグだった場合、そちらは空にする
            if source_position_id is not None:
                self.slot_assignments.pop(source_position_id, None)
                self.position_labels[source_position_id].config(
                    text=self.positions_by_id[source_position_id].name
                )

            self.slot_assignments[dropped_position_id] = crew
            dropped_position = self.positions_by_id[dropped_position_id]
            self.position_labels[dropped_position_id].config(
                text=f"{dropped_position.name}：{crew.name}"
            )

            if crew in self.available_crews:
                self.available_crews.remove(crew)

            self.refresh_crews()

        elif dropped_position_id is None and source_position_id is not None:
            # ポジション以外の場所へドロップ → 配置を解除してクルー一覧へ戻す
            self.slot_assignments.pop(source_position_id, None)
            self.position_labels[source_position_id].config(
                text=self.positions_by_id[source_position_id].name
            )

            if crew not in self.available_crews:
                self.available_crews.append(crew)

            self.refresh_crews()

        # 同じ場所に戻した場合や、クルー一覧からポジション以外へ
        # 落とした場合は何も変更しない

        if self.drag_label:
            self.drag_label.destroy()

        self.drag_label = None
        self.dragging_crew = None
        self.drag_source_position_id = None

    # --- 保存 ---

    def is_dirty(self) -> bool:
        """
        画面を開いた(または最後に保存した)時点の配置と、
        現在の下書きが異なっているかどうかを判定する。
        時間帯移動や「戻る」の際に、未保存の変更があるか確認するために使う。
        """
        current = {
            position_id: crew.id
            for position_id, crew in self.slot_assignments.items()
        }
        return current != self.initial_position_crew_ids

    def save_assignments(self):
        originally_assigned_position_ids = set(
            self.initial_position_crew_ids.keys()
        )

        for position in self.positions:
            pid = position.id

            if pid in self.slot_assignments:
                crew = self.slot_assignments[pid]
                try:
                    assign_crew_to_position(
                        self.date, self.time_slot_id, pid, crew.id
                    )
                except AssignmentConflictError as e:
                    messagebox.showerror("保存エラー", str(e))
                    return
            elif pid in originally_assigned_position_ids:
                delete_assignment(self.date, self.time_slot_id, pid)

        # 保存できたので「基準となる状態」を現在の下書きで更新する
        self.initial_position_crew_ids = {
            position_id: crew.id
            for position_id, crew in self.slot_assignments.items()
        }

        messagebox.showinfo("保存", "配置情報を保存しました")

    # --- 画面遷移（未保存確認つき） ---

    def confirm_discard_if_dirty(self) -> bool:
        """
        未保存の変更がある場合に確認ダイアログを出す。
        「はい」なら True（移動してよい）、「いいえ」なら False を返す。
        """
        if not self.is_dirty():
            return True

        return messagebox.askyesno(
            "確認",
            "保存されていない変更があります。保存せずに移動しますか？"
        )

    def handle_back(self):
        if not self.confirm_discard_if_dirty():
            return
        self.on_back()

    def prev_slot(self):
        if not self.confirm_discard_if_dirty():
            return

        previous = get_previous_time_slot(self.time_slot_id)

        if previous is not None:
            self.on_navigate(self.date, previous.id)
            return

        all_slots = get_all_time_slots()
        if not all_slots:
            messagebox.showerror("エラー", "時間帯データがありません")
            return

        new_date = self._shift_date(-1)
        self.on_navigate(new_date, all_slots[-1].id)

    def next_slot(self):
        if not self.confirm_discard_if_dirty():
            return

        nxt = get_next_time_slot(self.time_slot_id)

        if nxt is not None:
            self.on_navigate(self.date, nxt.id)
            return

        all_slots = get_all_time_slots()
        if not all_slots:
            messagebox.showerror("エラー", "時間帯データがありません")
            return

        new_date = self._shift_date(1)
        self.on_navigate(new_date, all_slots[0].id)

    def _shift_date(self, days: int) -> str:
        current = datetime.strptime(self.date, "%Y-%m-%d")
        new_date = current + timedelta(days=days)
        return new_date.strftime("%Y-%m-%d")