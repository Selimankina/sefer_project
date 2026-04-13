from src.renaming.schemas import RenameResult, RenameStatus


def build_report(results: list[RenameResult]) -> str:
    renamed = [r for r in results if r.status == RenameStatus.RENAMED]
    errors = [r for r in results if r.status == RenameStatus.ERROR]
    low_conf = [r for r in renamed if r.is_low_confidence]

    lines = []

    lines.append(f"Переименовано файлов: {len(renamed)}")
    lines.append("")

    lines.append(f"Низкая уверенность: {len(low_conf)}")
    for r in low_conf:
        lines.append(str(r.new_path))

    lines.append("")
    lines.append(f"Ошибки: {len(errors)}")
    for r in errors:
        lines.append(f"{r.image_path} -> {r.message}")

    return "\n".join(lines)