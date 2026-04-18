from pathlib import Path

from src.pipeline.state import PipelineStatus


def rename_file(state, duplicate_manager):
    old_path: Path = state.image_path
    status = state.status

    # --- определяем базовое имя ---
    if status == PipelineStatus.OK:
        base = state.new_name

    elif status == PipelineStatus.LOW_CONFIDENCE:
        base = state.new_name

    elif status in {
        PipelineStatus.NO_NUMBER,
        PipelineStatus.NO_DIGITS,
        PipelineStatus.NO_ROI,
        PipelineStatus.ERROR,
    }:
        base = old_path.stem

    else:
        base = old_path.stem

    # --- добавляем префикс !_ ---
    if status in {
        PipelineStatus.LOW_CONFIDENCE,
        PipelineStatus.NO_NUMBER,
        PipelineStatus.NO_DIGITS,
        PipelineStatus.NO_ROI,
    }:
        base = "!_" + base

    # --- учитываем дубликаты ---
    base = duplicate_manager.get_unique_name(base)

    new_filename = base + old_path.suffix
    new_path = old_path.with_name(new_filename)

    # --- защита от перезаписи ---
    if new_path.exists() and new_path != old_path:
        state.status = PipelineStatus.ERROR
        state.error_stage = "rename_conflict"
        state.error_message = f"{new_path.name} already exists"
        return

    try:
        old_path.rename(new_path)
        state.renamed_path = new_path

    except Exception as e:
        state.status = PipelineStatus.ERROR
        state.error_stage = "rename"
        state.error_message = str(e)