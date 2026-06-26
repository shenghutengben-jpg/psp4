import tkinter as tk
from tkinter import messagebox


class PositioningApp(tk.Tk):
    """
    ポジショニング管理システムのメインアプリ。
    画面遷移の中心になるクラス。
    """

    def __init__(self):
        super().__init__()

        self.title("ポジショニング管理システム")
        self.geometry("900x600")
        self.resizable(False, False)

        # 選択中の日付や時間帯を保持する
        self.selected_date = None
        self.selected_time_slot = None

        # 仮のクルーデータ
        # 後で CrewController から取得する形に変更する
        self.dummy_crews = [
            {"name": "Aさん", "start": "11:00", "end": "18:00"},
            {"name": "Bさん", "start": "16:00", "end": "24:00"},
            {"name": "Cさん", "start": "14:00", "end": "23:00"},
            {"name": "Dさん", "start": "17:00", "end": "21:00"},
        ]

        # 画面を表示するための共通フレーム
        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)

        # 最初の画面を表示
        self.show_calendar_view()

    def clear_screen(self):
        """現在表示している画面を削除する"""
        for widget in self.container.winfo_children():
            widget.destroy()

    # =========================
    # 1. カレンダー画面
    # =========================
    def show_calendar_view(self):
        self.clear_screen()

        title_label = tk.Label(
            self.container,
            text="ポジショニング管理システム",
            font=("Arial", 24, "bold")
        )
        title_label.pack(pady=40)

        instruction_label = tk.Label(
            self.container,
            text="日付を入力してください",
            font=("Arial", 14)
        )
        instruction_label.pack(pady=10)

        date_entry = tk.Entry(self.container, font=("Arial", 14), width=20)
        date_entry.insert(0, "2026/05/16")
        date_entry.pack(pady=10)

        def on_select_date():
            date = date_entry.get()

            if date == "":
                messagebox.showerror("入力エラー", "日付を入力してください")
                return

            self.selected_date = date
            self.show_crew_list_view()

        select_button = tk.Button(
            self.container,
            text="この日付で開始",
            font=("Arial", 14),
            width=20,
            command=on_select_date
        )
        select_button.pack(pady=30)

    # =========================
    # 2. クルー一覧画面
    # =========================
    def show_crew_list_view(self):
        self.clear_screen()

        title_label = tk.Label(
            self.container,
            text="クルー情報登録・編集画面",
            font=("Arial", 22, "bold")
        )
        title_label.pack(pady=20)

        date_label = tk.Label(
            self.container,
            text=f"選択日：{self.selected_date}",
            font=("Arial", 14)
        )
        date_label.pack(pady=10)

        list_frame = tk.Frame(self.container)
        list_frame.pack(pady=20)

        header = tk.Label(
            list_frame,
            text="クルー一覧",
            font=("Arial", 16, "bold")
        )
        header.grid(row=0, column=0, columnspan=3, pady=10)

        tk.Label(list_frame, text="名前", font=("Arial", 12, "bold"), width=15).grid(row=1, column=0)
        tk.Label(list_frame, text="出勤時間", font=("Arial", 12, "bold"), width=15).grid(row=1, column=1)
        tk.Label(list_frame, text="退勤時間", font=("Arial", 12, "bold"), width=15).grid(row=1, column=2)

        for index, crew in enumerate(self.dummy_crews, start=2):
            tk.Label(list_frame, text=crew["name"], font=("Arial", 12), width=15).grid(row=index, column=0)
            tk.Label(list_frame, text=crew["start"], font=("Arial", 12), width=15).grid(row=index, column=1)
            tk.Label(list_frame, text=crew["end"], font=("Arial", 12), width=15).grid(row=index, column=2)

        button_frame = tk.Frame(self.container)
        button_frame.pack(pady=30)

        add_button = tk.Button(
            button_frame,
            text="クルーを追加",
            font=("Arial", 12),
            width=18,
            command=self.show_crew_form_view
        )
        add_button.grid(row=0, column=0, padx=10)

        time_slot_button = tk.Button(
            button_frame,
            text="時間帯選択へ",
            font=("Arial", 12),
            width=18,
            command=self.show_time_slot_view
        )
        time_slot_button.grid(row=0, column=1, padx=10)

        back_button = tk.Button(
            button_frame,
            text="日付選択に戻る",
            font=("Arial", 12),
            width=18,
            command=self.show_calendar_view
        )
        back_button.grid(row=0, column=2, padx=10)

    # =========================
    # 3. クルー登録画面
    # =========================
    def show_crew_form_view(self):
        self.clear_screen()

        title_label = tk.Label(
            self.container,
            text="クルー登録画面",
            font=("Arial", 22, "bold")
        )
        title_label.pack(pady=30)

        form_frame = tk.Frame(self.container)
        form_frame.pack(pady=20)

        tk.Label(form_frame, text="名前", font=("Arial", 12), width=15).grid(row=0, column=0, pady=10)
        name_entry = tk.Entry(form_frame, font=("Arial", 12), width=25)
        name_entry.grid(row=0, column=1, pady=10)

        tk.Label(form_frame, text="出勤時間", font=("Arial", 12), width=15).grid(row=1, column=0, pady=10)
        start_entry = tk.Entry(form_frame, font=("Arial", 12), width=25)
        start_entry.insert(0, "17:00")
        start_entry.grid(row=1, column=1, pady=10)

        tk.Label(form_frame, text="退勤時間", font=("Arial", 12), width=15).grid(row=2, column=0, pady=10)
        end_entry = tk.Entry(form_frame, font=("Arial", 12), width=25)
        end_entry.insert(0, "21:00")
        end_entry.grid(row=2, column=1, pady=10)

        def on_register():
            name = name_entry.get()
            start_time = start_entry.get()
            end_time = end_entry.get()

            if name == "" or start_time == "" or end_time == "":
                messagebox.showerror("入力エラー", "すべての項目を入力してください")
                return

            # 今は仮でリストに追加
            # 後で CrewController.register_crew() に置き換える
            self.dummy_crews.append({
                "name": name,
                "start": start_time,
                "end": end_time
            })

            messagebox.showinfo("登録完了", "クルー情報を登録しました")
            self.show_crew_list_view()

        button_frame = tk.Frame(self.container)
        button_frame.pack(pady=30)

        register_button = tk.Button(
            button_frame,
            text="登録する",
            font=("Arial", 12),
            width=15,
            command=on_register
        )
        register_button.grid(row=0, column=0, padx=10)

        back_button = tk.Button(
            button_frame,
            text="戻る",
            font=("Arial", 12),
            width=15,
            command=self.show_crew_list_view
        )
        back_button.grid(row=0, column=1, padx=10)

    # =========================
    # 4. 時間帯選択画面
    # =========================
    def show_time_slot_view(self):
        self.clear_screen()

        title_label = tk.Label(
            self.container,
            text="時間帯選択画面",
            font=("Arial", 22, "bold")
        )
        title_label.pack(pady=30)

        time_slots = [
            "00:00〜01:00",
            "01:00〜02:00",
            "02:00〜03:00",
            "03:00〜04:00",
            "04:00〜05:00",
            "05:00〜06:00",
            "06:00〜07:00",
            "07:00〜08:00",
            "08:00〜09:00",
            "09:00〜10:00",
            "10:00〜11:00",
            "11:00〜12:00",
            "12:00〜13:00",
            "13:00〜14:00",
            "14:00〜15:00",
            "15:00〜16:00",
            "16:00〜17:00",
            "17:00〜18:00",
            "18:00〜19:00",
            "19:00〜20:00",
            "20:00〜21:00",
            "21:00〜22:00",
            "22:00〜23:00",
            "23:00〜24:00"
        ]

        def on_select_time_slot(time_slot):
            self.selected_time_slot = time_slot
            self.show_position_edit_view()

        for time_slot in time_slots:
            button = tk.Button(
                self.container,
                text=time_slot,
                font=("Arial", 14),
                width=25,
                command=lambda ts=time_slot: on_select_time_slot(ts)
            )
            button.pack(pady=8)

        back_button = tk.Button(
            self.container,
            text="クルー一覧に戻る",
            font=("Arial", 12),
            width=20,
            command=self.show_crew_list_view
        )
        back_button.pack(pady=30)

    # =========================
    # 5. ポジション編集画面
    # =========================
    def show_position_edit_view(self):
        self.clear_screen()

        title_label = tk.Label(
            self.container,
            text="ポジション編集画面",
            font=("Arial", 22, "bold")
        )
        title_label.pack(pady=20)

        info_label = tk.Label(
            self.container,
            text=f"日付：{self.selected_date}　時間帯：{self.selected_time_slot}",
            font=("Arial", 14)
        )
        info_label.pack(pady=10)

        main_frame = tk.Frame(self.container)
        main_frame.pack(pady=20)

        # 左側：クルー一覧
        crew_frame = tk.LabelFrame(main_frame, text="勤務中クルー", font=("Arial", 12))
        crew_frame.grid(row=0, column=0, padx=30)

        for crew in self.dummy_crews:
            tk.Label(
                crew_frame,
                text=f'{crew["name"]}（{crew["start"]}〜{crew["end"]}）',
                font=("Arial", 11),
                width=25
            ).pack(pady=5)

        # 右側：ポジション一覧
        position_frame = tk.LabelFrame(main_frame, text="ポジション", font=("Arial", 12))
        position_frame.grid(row=0, column=1, padx=30)

        positions = ["カウンター", "カウンターランナー", "オーダーテイカー", "キャッシャー", "ポテト", "イニシエーター", "ストッカー", "アッセンブラー", "休憩"]

        for position in positions:
            tk.Label(
                position_frame,
                text=position,
                font=("Arial", 11),
                width=20,
                relief="solid"
            ).pack(pady=5)

        button_frame = tk.Frame(self.container)
        button_frame.pack(pady=30)

        save_button = tk.Button(
            button_frame,
            text="保存する",
            font=("Arial", 12),
            width=15,
            command=lambda: messagebox.showinfo("保存", "配置情報を保存しました")
        )
        save_button.grid(row=0, column=0, padx=10)

        back_button = tk.Button(
            button_frame,
            text="時間帯選択に戻る",
            font=("Arial", 12),
            width=18,
            command=self.show_time_slot_view
        )
        back_button.grid(row=0, column=1, padx=10)


def main():
    app = PositioningApp()
    app.mainloop()


if __name__ == "__main__":
    main()