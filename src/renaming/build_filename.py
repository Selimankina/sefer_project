from pathlib import Path


def build_filename(
    base_name: str,
    original_path: Path,
    add_low_confidence_mark: bool = False,
) -> str:
    """
    Формирует имя файла:
    - добавляет "!_" при необходимости
    - сохраняет расширение
    """
    name = base_name

    if add_low_confidence_mark:
        name = f"!_{name}"

    return f"{name}{original_path.suffix.lower()}"