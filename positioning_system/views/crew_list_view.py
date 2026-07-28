"""
クルー勤務一覧画面。

指定した日付に登録されている勤務予定(Schedule)の一覧を表示する。
"""

import tkinter as tk
from tkinter import ttk, messagebox

from controllers import (
    get_schedules_by_date,
    get_crew_by_id,
    delete_schedule,
    update_schedule,
)


class CrewListView(tk.Frame):
    def __init__(self, master, get_selected_date, on_next, on_back):
        super().__init__(master)

        self.get_selected_date = get_selected_date
        self.on_next = on_next
        self.on_back = on_back

        tk.Label(
            self,
            text="クルー勤務一覧画面",
            font=("Arial", 18)
        ).pack(pady=20)

        self.date_label = tk.Label(
            self,
            text=f"選択日: {self.get_selected_date()}"
        )
        self.date_label.pack(pady=5)

        self.tree = ttk.Treeview(
            self,
            columns=("crew_name", "start_time", "end_time"),
            show="headings",
            height=12
        )

        self.tree.heading("crew_name", text="クルー名")
        self.tree.heading("start_time", text="出勤時間")
        self.tree.heading("end_time", text="退勤時間")

        self.tree.column("crew_name", width=180)
        self.tree.column("start_time", width=120)
        self.tree.column("end_time", width=120)

        self.tree.pack(pady=10)

        button_frame = tk.Frame(self)
        button_frame.pack(pady=10)

        tk.Button(
            button_frame,
            text="一覧更新",
            command=self.refresh
        ).grid(row=0, column=0, padx=5)

        tk.Button(
            button_frame,
            text="選択した勤務予定を編集",
            command=self.edit_selected_schedule
        ).grid(row=0, column=1, padx=5)

        tk.Button(
            button_frame,
            text="選択した勤務予定を削除",
            command=self.delete_selected_schedule
        ).grid(row=0, column=2, padx=5)

        tk.Button(
            button_frame,
            text="勤務登録へ戻る",
            command=self.on_back
        ).grid(row=0, column=3, padx=5)

        tk.Button(
            button_frame,
            text="時間帯選択へ",
            command=self.on_next
        ).grid(row=0, column=4, padx=5)

        self.refresh()

    def refresh(self):
        date = self.get_selected_date()

        if not date:
            messagebox.showerror(
                "エラー",
                "日付が選択されていません"
            )
            return

        self.date_label.config(text=f"選択日: {date}")

        # 現在の一覧を削除
        for item in self.tree.get_children():
            self.tree.delete(item)

        schedules = get_schedules_by_date(date)

        for schedule in schedules:
            crew = get_crew_by_id(schedule.crew_id)

            crew_name = (
                crew.name
                if crew is not None
                else "不明なクルー"
            )

            self.tree.insert(
                "",
                tk.END,

                # Treeviewの行IDとしてScheduleのIDを保存
                iid=str(schedule.id),

                values=(
                    crew_name,
                    schedule.start_time,
                    schedule.end_time
                )
            )

    def edit_selected_schedule(self):
        selected_items = self.tree.selection()

        if not selected_items:
            messagebox.showerror(
                "エラー",
                "編集する勤務予定を選択してください"
            )
            return

        # Treeviewのiidにはschedule.idを入れている
        schedule_id = int(selected_items[0])

        # 選択した行の表示内容を取得
        values = self.tree.item(
            selected_items[0],
            "values"
        )

        crew_name = values[0]
        start_time = values[1]
        end_time = values[2]

        # 編集用ウィンドウ
        edit_window = tk.Toplevel(self)
        edit_window.title("勤務予定編集")
        edit_window.geometry("350x300")

        tk.Label(
            edit_window,
            text="勤務予定編集",
            font=("Arial", 16)
        ).pack(pady=15)

        tk.Label(
            edit_window,
            text="クルー名"
        ).pack()

        name_entry = tk.Entry(
            edit_window,
            width=30
        )
        name_entry.insert(0, crew_name)
        name_entry.pack(pady=5)

        tk.Label(
            edit_window,
            text="出勤時間"
        ).pack()

        start_entry = tk.Entry(
            edit_window,
            width=30
        )
        start_entry.insert(0, start_time)
        start_entry.pack(pady=5)

        tk.Label(
            edit_window,
            text="退勤時間"
        ).pack()

        end_entry = tk.Entry(
            edit_window,
            width=30
        )
        end_entry.insert(0, end_time)
        end_entry.pack(pady=5)

        def save_edit():
            new_crew_name = name_entry.get().strip()
            new_start_time = start_entry.get().strip()
            new_end_time = end_entry.get().strip()

            if not new_crew_name:
                messagebox.showerror(
                    "エラー",
                    "クルー名を入力してください",
                    parent=edit_window
                )
                return

            if not self.is_valid_time(new_start_time):
                messagebox.showerror(
                    "エラー",
                    "出勤時間を HH:MM 形式で入力してください",
                    parent=edit_window
                )
                return

            if not self.is_valid_time(new_end_time):
                messagebox.showerror(
                    "エラー",
                    "退勤時間を HH:MM 形式で入力してください",
                    parent=edit_window
                )
                return

            if new_start_time >= new_end_time:
                messagebox.showerror(
                    "エラー",
                    "退勤時間は出勤時間より後にしてください",
                    parent=edit_window
                )
                return

            result = update_schedule(
                schedule_id=schedule_id,
                crew_name=new_crew_name,
                start_time=new_start_time,
                end_time=new_end_time,
            )

            if result is None:
                messagebox.showerror(
                    "エラー",
                    "編集対象の勤務予定が見つかりません",
                    parent=edit_window
                )
                return

            messagebox.showinfo(
                "編集完了",
                "勤務予定を編集しました",
                parent=edit_window
            )

            edit_window.destroy()

            # 一覧を更新
            self.refresh()

        tk.Button(
            edit_window,
            text="変更を保存",
            command=save_edit
        ).pack(pady=15)

    def delete_selected_schedule(self):
        selected_items = self.tree.selection()

        if not selected_items:
            messagebox.showerror(
                "エラー",
                "削除する勤務予定を選択してください"
            )
            return

        schedule_id = int(selected_items[0])

        answer = messagebox.askyesno(
            "削除確認",
            "選択した勤務予定を削除しますか？"
        )

        if not answer:
            return

        delete_schedule(schedule_id)

        messagebox.showinfo(
            "削除完了",
            "勤務予定を削除しました"
        )

        # 削除後に一覧を更新
        self.refresh()

    def is_valid_time(self, time_str: str) -> bool:
        """
        HH:MM形式の時刻かどうかを確認する。
        24:00は許可する。
        """

        parts = time_str.split(":")

        if len(parts) != 2:
            return False

        hour_str, minute_str = parts

        if not (
            hour_str.isdigit()
            and minute_str.isdigit()
        ):
            return False

        if len(hour_str) != 2:
            return False

        if len(minute_str) != 2:
            return False

        hour = int(hour_str)
        minute = int(minute_str)

        if minute > 59:
            return False

        if hour == 24:
            return minute == 0

        return 0 <= hour <= 23