from pathlib import Path

from src.pipeline.state import PipelineStatus


UNRELIABLE_STATUSES = {
    PipelineStatus.LOW_CONFIDENCE,
    PipelineStatus.NO_NUMBER,
    PipelineStatus.NO_DIGITS,
    PipelineStatus.NO_ROI,
    PipelineStatus.PREPROCESS_ERROR,
}


def rename_file(state, duplicate_manager):
    old_path: Path = state.image_path
    status = state.status

    # --- базовое имя ---
    if status in {PipelineStatus.OK, PipelineStatus.LOW_CONFIDENCE}:
        base = state.new_name
    else:
        base = old_path.stem

    # fallback
    if not base:
        base = old_path.stem

    # --- префикс для ненадёжных результатов ---
    if status in UNRELIABLE_STATUSES:
        base = "!_" + base

    # --- обработка дубликатов ---
    base = duplicate_manager.get_unique_name(base)

    new_filename = base + old_path.suffix
    new_path = old_path.with_name(new_filename)

    # --- защита от перезаписи ---
    if new_path.exists() and new_path != old_path:
        state.status = PipelineStatus.ERROR
        state.error_stage = "rename_conflict"
        state.error_message = f"{new_path.name} already exists"
        return

    # --- переименование ---
    try:
        old_path.rename(new_path)

        state.renamed_path = new_path
        state.new_name = new_path.stem
        state.error_stage = None
        state.error_message = None

    except Exception as e:
        state.status = PipelineStatus.ERROR
        state.error_stage = "rename"
        state.error_message = str(e)