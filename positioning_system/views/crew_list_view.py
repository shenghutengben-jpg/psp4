import tkinter as tk
from tkinter import ttk, messagebox

from controllers.date_controller import get_schedules_by_date
from controllers.date_controller import update_schedule
from controllers.date_controller import delete_schedule
from controllers.crew_controller import get_crew_by_id


class CrewListView(tk.Frame):
    def __init__(self, master, get_selected_date, on_next, on_back):
        super().__init__(master)

        self.get_selected_date = get_selected_date
        self.on_next = on_next
        self.on_back = on_back

        self.schedules = []

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
            height=10
        )

        self.tree.heading("crew_name", text="クルー名")
        self.tree.heading("start_time", text="出勤時間")
        self.tree.heading("end_time", text="退勤時間")

        self.tree.column("crew_name", width=180)
        self.tree.column("start_time", width=120)
        self.tree.column("end_time", width=120)

        self.tree.pack(pady=10)

        self.tree.bind("<<TreeviewSelect>>", self.on_schedule_selected)

        edit_frame = tk.Frame(self)
        edit_frame.pack(pady=10)

        tk.Label(edit_frame, text="クルー名").grid(row=0, column=0, padx=5)
        self.name_entry = tk.Entry(edit_frame, width=20)
        self.name_entry.grid(row=0, column=1, padx=5)

        tk.Label(edit_frame, text="出勤時間").grid(row=1, column=0, padx=5)
        self.start_combo = ttk.Combobox(
            edit_frame,
            values=self.create_time_options(),
            state="readonly",
            width=18
        )
        self.start_combo.grid(row=1, column=1, padx=5)

        tk.Label(edit_frame, text="退勤時間").grid(row=2, column=0, padx=5)
        self.end_combo = ttk.Combobox(
            edit_frame,
            values=self.create_time_options(),
            state="readonly",
            width=18
        )
        self.end_combo.grid(row=2, column=1, padx=5)

        button_frame = tk.Frame(self)
        button_frame.pack(pady=10)

        tk.Button(
            button_frame,
            text="一覧更新",
            command=self.refresh
        ).grid(row=0, column=0, padx=5)

        tk.Button(
            button_frame,
            text="編集",
            command=self.edit_selected_schedule
        ).grid(row=0, column=1, padx=5)

        tk.Button(
            button_frame,
            text="削除",
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

    def create_time_options(self):
        options = []

        for hour in range(24):
            options.append(f"{hour:02d}:00")

        options.append("24:00")

        return options

    def refresh(self):
        date = self.get_selected_date()

        if not date:
            messagebox.showerror("エラー", "日付が選択されていません")
            return

        self.date_label.config(text=f"選択日: {date}")

        for item in self.tree.get_children():
            self.tree.delete(item)

        self.schedules = get_schedules_by_date(date)

        for schedule in self.schedules:
            crew = get_crew_by_id(schedule["crew_id"])

            if crew is None:
                crew_name = "不明なクルー"
            else:
                crew_name = crew["name"]

            self.tree.insert(
                "",
                tk.END,
                iid=str(schedule["id"]),
                values=(
                    crew_name,
                    schedule["start_time"],
                    schedule["end_time"]
                )
            )

    def get_selected_schedule_id(self):
        selected = self.tree.selection()

        if not selected:
            return None

        return int(selected[0])

    def on_schedule_selected(self, event):
        selected_id = self.get_selected_schedule_id()

        if selected_id is None:
            return

        for schedule in self.schedules:
            if schedule["id"] == selected_id:
                crew = get_crew_by_id(schedule["crew_id"])

                if crew is None:
                    crew_name = ""
                else:
                    crew_name = crew["name"]

                self.name_entry.delete(0, tk.END)
                self.name_entry.insert(0, crew_name)

                self.start_combo.set(schedule["start_time"])
                self.end_combo.set(schedule["end_time"])

                return

    def edit_selected_schedule(self):
        schedule_id = self.get_selected_schedule_id()

        if schedule_id is None:
            messagebox.showerror("エラー", "編集するクルーを選択してください")
            return

        crew_name = self.name_entry.get().strip()
        start_time = self.start_combo.get()
        end_time = self.end_combo.get()

        if not crew_name:
            messagebox.showerror("エラー", "クルー名を入力してください")
            return

        if not start_time or not end_time:
            messagebox.showerror("エラー", "出勤時間と退勤時間を選択してください")
            return

        try:
            result = update_schedule(
                schedule_id=schedule_id,
                crew_name=crew_name,
                start_time=start_time,
                end_time=end_time
            )

        except ValueError as e:
            messagebox.showerror("入力エラー", str(e))
            return

        if result is None:
            messagebox.showerror("エラー", "編集対象が見つかりません")
            return

        messagebox.showinfo("編集完了", "勤務予定を編集しました")
        self.refresh()

    def delete_selected_schedule(self):
        schedule_id = self.get_selected_schedule_id()

        if schedule_id is None:
            messagebox.showerror("エラー", "削除するクルーを選択してください")
            return

        answer = messagebox.askyesno(
            "削除確認",
            "選択した勤務予定を削除しますか？"
        )

        if not answer:
            return

        delete_schedule(schedule_id)

        messagebox.showinfo("削除完了", "勤務予定を削除しました")

        self.name_entry.delete(0, tk.END)
        self.start_combo.set("")
        self.end_combo.set("")

        self.refresh()