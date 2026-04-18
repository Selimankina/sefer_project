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
    existing_names = {p.stem for p in input_dir.glob("*") if p.is_file()}
    manager = DuplicateManager(existing_names)

    for image_path in sorted(input_dir.glob("*")):
        state = PipelineState(image_path=str(image_path))

        # --- load ---
        image = load_image(image_path)
        if image is None:
            state.status = PipelineStatus.LOAD_ERROR
            state.should_mark_unreliable = True
            yield state
            continue

        state.image = image

        # --- ROI ---
        roi = process_roi(image)
        if roi is None:
            state.status = PipelineStatus.NO_ROI
            state.should_mark_unreliable = True
            yield state
            continue

        state.roi = roi

        # --- preprocess ---
        processed, meta = process_preprocessing(image, roi)

        if processed is None:
            state.status = PipelineStatus.PREPROCESS_ERROR
            state.preprocessing_meta = meta
            state.should_mark_unreliable = True
            yield state
            continue

        state.processed_image = processed
        state.preprocessing_meta = meta

        # --- digits ---
        digits = detect_digits(processed)

        if digits is None or len(digits) == 0:
            state.status = PipelineStatus.NO_DIGITS
            state.should_mark_unreliable = True
            yield state
            continue

        state.digits = digits

        # --- assembly ---
        number, confidence, meta = assemble_number(digits)

        state.number = number
        state.confidence = confidence

        # --- decision ---
        if number is None:
            state.status = PipelineStatus.NO_NUMBER
            state.should_mark_unreliable = True
        elif confidence < MIN_CONFIDENCE:
            state.status = PipelineStatus.LOW_CONFIDENCE
            state.should_mark_unreliable = True
        else:
            state.status = PipelineStatus.OK

        # --- naming ---
        if number is not None:
            state.new_name = format_number(number)

        # --- rename ---
        rename_file(state, manager)

        yield state