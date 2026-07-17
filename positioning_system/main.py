"""
ポジショニング管理システム アプリケーションのエントリーポイント。

【この統合版での変更点】
- 以前は本番用main.py（PositioningApp・ダミーデータ使用）と
  デバッグ用main.py（DebugApp・JSON永続化あり）の2系統が
  並行して存在していたが、この統合版はデバッグ用側で検証していた
  「views(tk.Frame+コールバック方式) + controllers + repositories」
  の構成を正式な本番構成として採用し、1本にまとめている。
- dummy_crews は廃止。クルー情報はすべて controllers 経由で
  JSON(data/crews.json 等)へ永続化される。
- 初回起動時、positions.json / time_slots.json が空であれば
  デフォルトのマスタデータを自動投入する(seed_initial_data)。
  これは以前 position_edit_view.py にハードコードされていた
  9つのポジション名と、24時間分の時間帯に対応する。
"""

import tkinter as tk

from views import (
    CalendarView,
    CrewFormView,
    CrewListView,
    TimeSlotView,
    PositionEditView,
)
from controllers import get_all_positions, get_all_time_slots
from repositories import save_positions, save_time_slots
from models import Position, TimeSlot


DEFAULT_POSITION_NAMES = [
    "カウンター",
    "カウンターランナー",
    "オーダーテイカー",
    "キャッシャー",
    "ポテト",
    "イニシ",
    "アッセンブラー",
    "ストッカー",
    "休憩",
]


def seed_initial_data():
    """
    初回起動時、マスタデータ(ポジション・時間帯)が1件も無ければ
    デフォルトのデータを投入する。
    2回目以降の起動では、既にデータがあるため何もしない。
    """
    if not get_all_positions():
        positions = [
            Position(id=index + 1, name=name)
            for index, name in enumerate(DEFAULT_POSITION_NAMES)
        ]
        save_positions(positions)

    if not get_all_time_slots():
        time_slots = []
        for hour in range(24):
            start_time = f"{hour:02}:00"
            end_time = f"{hour + 1:02}:00"  # 最後は "24:00" になる
            time_slots.append(
                TimeSlot(id=hour + 1, start_time=start_time, end_time=end_time)
            )
        save_time_slots(time_slots)


class PositioningApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("ポジショニング管理システム")
        self.geometry("1200x800")

        # ウィンドウサイズを固定し、最大化・リサイズを禁止する。
        # pack()は中身のサイズにぴったり合わせて配置されるため、
        # ウィンドウだけを大きくすると中身とのバランスが崩れて見える
        # 不具合があったため、この対応で固定している。
        self.resizable(False, False)

        # アプリ全体で共有する状態。
        # 各Viewへは直接この変数を渡さず、get_selected_date等の
        # コールバック関数を渡すことで、Viewからは読み取り専用に
        # アクセスできるようにしている。
        self.selected_date = None
        self.selected_time_slot_id = None

        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)

        self.current_frame = None

        self.show_calendar_view()

    # --- 状態の取得・更新 ---

    def get_selected_date(self):
        return self.selected_date

    def get_selected_time_slot_id(self):
        return self.selected_time_slot_id

    def set_date(self, date):
        self.selected_date = date
        self.show_crew_form_view()

    def set_time_slot(self, time_slot_id):
        self.selected_time_slot_id = time_slot_id
        self.show_position_edit_view()

    def navigate_position_edit(self, date, time_slot_id):
        """
        PositionEditView内の「前後の時間帯へ移動する」から呼ばれる。
        日付をまたぐ場合もあるため、date・time_slot_idの両方を
        まとめて更新してから再描画する。
        """
        self.selected_date = date
        self.selected_time_slot_id = time_slot_id
        self.show_position_edit_view()

    # --- 画面遷移 ---

    def clear_screen(self):
        if self.current_frame is not None:
            self.current_frame.destroy()
            self.current_frame = None

    def show_calendar_view(self):
        self.clear_screen()
        self.current_frame = CalendarView(
            self.container,
            on_date_selected=self.set_date,
        )
        self.current_frame.pack(fill="both", expand=True)

    def show_crew_form_view(self):
        self.clear_screen()
        self.current_frame = CrewFormView(
            self.container,
            get_selected_date=self.get_selected_date,
            on_next=self.show_crew_list_view,
            on_back=self.show_calendar_view,
        )
        self.current_frame.pack(fill="both", expand=True)

    def show_crew_list_view(self):
        self.clear_screen()
        self.current_frame = CrewListView(
            self.container,
            get_selected_date=self.get_selected_date,
            on_next=self.show_time_slot_view,
            on_back=self.show_crew_form_view,
        )
        self.current_frame.pack(fill="both", expand=True)

    def show_time_slot_view(self):
        self.clear_screen()
        self.current_frame = TimeSlotView(
            self.container,
            get_selected_date=self.get_selected_date,
            on_time_slot_selected=self.set_time_slot,
            on_back=self.show_crew_list_view,
        )
        self.current_frame.pack(fill="both", expand=True)

    def show_position_edit_view(self):
        self.clear_screen()
        self.current_frame = PositionEditView(
            self.container,
            get_selected_date=self.get_selected_date,
            get_selected_time_slot_id=self.get_selected_time_slot_id,
            on_navigate=self.navigate_position_edit,
            on_back=self.show_time_slot_view,
        )
        self.current_frame.pack(fill="both", expand=True)


def main():
    seed_initial_data()

    app = PositioningApp()
    app.mainloop()


if __name__ == "__main__":
    main()