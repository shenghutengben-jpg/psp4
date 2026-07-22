"""
ポジション（マスタ情報）を管理するコントローラー。

【追加の経緯】
views（特にポジション編集画面）を実装する過程で、ポジション一覧を
これまでのようにView側にハードコードした文字列リストとしてではなく、
positions.json のマスタデータから取得する必要があることに気づいたため、
今回新たに追加した。crew_controller.py と同じ構成にしている。
"""

from models import Position
from repositories.position_repository import load_positions, save_positions


def get_all_positions():
    return load_positions()


def get_position_by_id(position_id: int):
    for position in load_positions():
        if position.id == position_id:
            return position
    return None


def _generate_new_id(positions):
    if not positions:
        return 1
    return max(position.id for position in positions) + 1


def add_position(name: str) -> Position:
    positions = load_positions()

    new_position = Position(
        id=_generate_new_id(positions),
        name=name,
    )

    positions.append(new_position)
    save_positions(positions)

    return new_position


def delete_position(position_id: int) -> None:
    positions = load_positions()
    remaining = [p for p in positions if p.id != position_id]
    save_positions(remaining)