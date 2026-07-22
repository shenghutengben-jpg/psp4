"""
クルーのマスタ情報（Crew）を管理するコントローラー。

クルーの新規登録・取得・削除はすべてここに集約する。
以前は schedule_controller（旧date_controller）側にも
get_or_create_crew という名前でほぼ同じロジックが存在していたため、
ここに統合した。
"""

from models import Crew
from repositories.crew_repository import load_crews, save_crews


def get_all_crews() -> list[Crew]:
    return load_crews()


def get_crew_by_id(crew_id: int) -> Crew | None:
    crews = load_crews()

    for crew in crews:
        if crew.id == crew_id:
            return crew

    return None


def get_crew_by_name(name: str) -> Crew | None:
    """
    氏名からクルーを検索する。

    注意: 氏名だけで同一人物と判定しているため、
    同姓同名の別人がいる場合は区別できない。
    運用上問題になりそうであれば、クルーIDを別途
    入力・選択させる方式への変更を検討したい。
    """
    crews = load_crews()

    for crew in crews:
        if crew.name == name:
            return crew

    return None


def _generate_new_id(crews: list[Crew]) -> int:
    if not crews:
        return 1
    return max(crew.id for crew in crews) + 1


def add_crew(name: str) -> Crew:
    crews = load_crews()

    new_crew = Crew(
        id=_generate_new_id(crews),
        name=name,
    )

    crews.append(new_crew)
    save_crews(crews)

    return new_crew


def get_or_create_crew(name: str) -> Crew:
    """
    氏名が一致するクルーがいればそれを返し、
    いなければ新規登録して返す。
    """
    existing = get_crew_by_name(name)
    if existing is not None:
        return existing

    return add_crew(name)


def delete_crew(crew_id: int) -> None:
    crews = load_crews()
    remaining = [crew for crew in crews if crew.id != crew_id]
    save_crews(remaining)