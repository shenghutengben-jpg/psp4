"""
時間帯選択画面。

選択済みの日付に対して、ポジション編集を行いたい時間帯を選ぶ画面。
時間帯マスタ(TimeSlot)はcontrollers.get_all_time_slotsから取得する
実データを使用する（以前のapp.container版ではmain.py側で24時間分の
ダミー文字列を直接生成していたが、実データに置き換えた）。
"""

import tkinter as tk

from controllers import get_all_time_slots


class TimeSlotView(tk.Frame):
    def __init__(self, master, get_selected_date, on_time_slot_selected, on_back):
        super().__init__(master)

        self.get_selected_date = get_selected_date
        self.on_time_slot_selected = on_time_slot_selected
        self.on_back = on_back

        tk.Label(self, text="時間帯選択", font=("Arial", 22, "bold")).pack(pady=20)

        date = self.get_selected_date()
        tk.Label(self, text=f"選択日: {date}", font=("Arial", 12)).pack()

        tk.Label(
            self,
            text="ポジショニングを行う時間帯を選択してください。",
            font=("Arial", 12)
        ).pack(pady=5)

        time_slots = get_all_time_slots()

        if not time_slots:
            tk.Label(
                self,
                text="時間帯データが登録されていません。",
                fg="red"
            ).pack(pady=20)
        else:
            frame = tk.Frame(self)
            frame.pack()

            for index, time_slot in enumerate(time_slots):
                row = index // 3
                col = index % 3

                label_text = f"{time_slot.start_time}〜{time_slot.end_time}"

                tk.Button(
                    frame,
                    text=label_text,
                    width=18,
                    command=lambda ts=time_slot: self.on_time_slot_selected(ts.id)
                ).grid(row=row, column=col, padx=5, pady=5)

        tk.Button(self, text="戻る", command=self.on_back).pack(pady=20)