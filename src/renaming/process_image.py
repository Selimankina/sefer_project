from pathlib import Path

from src.number_recognition.schemas import NumberResult, NumberStatus
from src.renaming.format_number import format_number  # ✅ исправили импорт
from src.renaming.build_filename import build_filename
from src.renaming.duplicate_manager import DuplicateManager
from src.renaming.schemas import RenameResult, RenameStatus
from src.utils.logger import setup_logger


logger = setup_logger()


def _should_add_mark(path: Path) -> bool:
    """
    Проверяет, нужно ли добавлять '!_'
    """
    return not path.name.startswith("!_")


def process_image(
    result: NumberResult,
    duplicate_manager: DuplicateManager,
    apply: bool = False,
) -> RenameResult:
    original_path = result.image_path

    try:
        add_mark = False
        base_name: str | None = None

        # --- определяем стратегию ---
        if result.status in {
            NumberStatus.OK,
            NumberStatus.LOW_CONFIDENCE,
        }:
            formatted = format_number(result.formatted_number)

            if formatted is None:
                # ❗ невалидный номер (например 0000)
                base_name = original_path.stem
                add_mark = True
            else:
                base_name = formatted
                add_mark = result.status == NumberStatus.LOW_CONFIDENCE

        else:
            # NO_NUMBER / INVALID_FORMAT / ERROR
            base_name = original_path.stem
            add_mark = True

        # --- защита от повторного '!_' ---
        if add_mark and not _should_add_mark(original_path):
            add_mark = False

        # --- формирование имени ---
        filename = build_filename(
            base_name,
            original_path,
            add_low_confidence_mark=add_mark,
        )

        # --- уникализация ---
        filename = duplicate_manager.get_unique_name(filename)

        new_path = original_path.with_name(filename)

        # --- лог ---
        logger.info(
            f"{original_path.name} -> {filename} "
            f"(status={result.status}, conf={result.confidence})"
        )

        # --- применение ---
        if apply:
            original_path.rename(new_path)
        else:
            logger.info("[DRY-RUN] rename skipped")

        return RenameResult(
            image_path=original_path,
            new_path=new_path,
            status=RenameStatus.RENAMED,
            is_low_confidence=add_mark,
        )

    except Exception as e:
        logger.error(f"{original_path} -> ERROR: {e}")

        return RenameResult(
            image_path=original_path,
            new_path=None,
            status=RenameStatus.ERROR,
            message=str(e),
        )