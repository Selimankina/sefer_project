from pathlib import Path
from collections.abc import Generator

from src.number_recognition.process_folder import process_number_recognition
from src.renaming.process_folder import process_folder as process_renaming
from src.renaming.schemas import RenameResult


def process_pipeline(
    folder_path: Path,
    apply: bool = False,
) -> Generator[RenameResult, None, None]:
    """
    Полный pipeline:
    folder → ROI → preprocessing → digits → number → renaming
    """

    number_results = process_number_recognition(folder_path)

    yield from process_renaming(
        number_results,
        apply=apply,
    )