from collections.abc import Generator, Iterable

from src.number_recognition.schemas import NumberResult
from src.renaming.duplicate_manager import DuplicateManager
from src.renaming.process_image import process_image
from src.renaming.schemas import RenameResult


def process_folder(
    results: Iterable[NumberResult],  # 🔥 было list → стало Iterable
    apply: bool = False,
) -> Generator[RenameResult, None, None]:
    duplicate_manager = DuplicateManager()

    for result in results:
        yield process_image(
            result,
            duplicate_manager=duplicate_manager,
            apply=apply,
        )