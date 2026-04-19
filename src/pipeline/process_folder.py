from pathlib import Path

from src.pipeline.state import PipelineState, PipelineStatus
from src.pipeline.io import load_image
from src.roi_detection.process_image import process_roi
from src.preprocessing.process_image import process_preprocessing
from src.digits_detection.detector import detect_digits
from src.number_assembly.assembler import assemble_number

from src.common.formatting import format_number
from config.settings import MIN_CONFIDENCE

from src.renaming.process_image import rename_file
from src.renaming.duplicate_manager import DuplicateManager


def process_folder(input_dir: Path):
    """
        Обрабатывает все изображения в папке через полный пайплайн.

        Последовательно выполняет:
        - загрузку изображения
        - поиск ROI
        - предобработку
        - детекцию цифр
        - сборку номера
        - переименование файла

        Каждый шаг сохраняет результат в PipelineState.
        В случае ошибки этап помечается статусом, и обработка файла продолжается
        с переходом к переименованию.

        Args:
            input_dir (Path): Папка с изображениями.

        Yields:
            PipelineState: Состояние обработки для каждого файла.
        """

    # Собираем уже существующие имена файлов, чтобы избегать конфликтов
    existing_names = {p.stem for p in input_dir.glob("*") if p.is_file()}
    manager = DuplicateManager(existing_names)

    for image_path in sorted(input_dir.glob("*")):
        state = PipelineState(image_path=image_path)

        # --- загрузка изображения ---
        image = load_image(image_path)
        if image is None:
            state.status = PipelineStatus.LOAD_ERROR
            state.should_mark_unreliable = True
            rename_file(state, manager)
            yield state
            continue

        state.image = image

        # --- поиск ROI ---
        roi = process_roi(image)
        if roi is None:
            state.status = PipelineStatus.NO_ROI
            state.should_mark_unreliable = True
            rename_file(state, manager)
            yield state
            continue

        state.roi = roi

        # --- предобработка ---
        processed, meta = process_preprocessing(image, roi)
        if processed is None:
            state.status = PipelineStatus.PREPROCESS_ERROR
            state.preprocessing_meta = meta
            state.should_mark_unreliable = True
            rename_file(state, manager)
            yield state
            continue

        state.processed_image = processed

        # --- детекция цифр ---
        digits = detect_digits(processed)
        if not digits:
            state.status = PipelineStatus.NO_DIGITS
            state.should_mark_unreliable = True
            rename_file(state, manager)
            yield state
            continue

        state.digits = digits

        # --- сборка номера ---
        number, confidence, meta = assemble_number(digits)

        state.number = number
        state.confidence = confidence

        # --- переименование файла ---
        if number is None:
            state.status = PipelineStatus.NO_NUMBER
            state.should_mark_unreliable = True

        else:
            state.new_name = format_number(number)

            if confidence < MIN_CONFIDENCE:
                state.status = PipelineStatus.LOW_CONFIDENCE
                state.should_mark_unreliable = True
            else:
                state.status = PipelineStatus.OK

        rename_file(state, manager)

        yield state