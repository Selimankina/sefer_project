from pathlib import Path

from src.roi_detection.process_image import roi_detection_image

SUPPORTED_EXT = {".jpg", ".jpeg", ".png"}


def is_supported_file(path: Path) -> bool:
    return path.suffix.lower() in SUPPORTED_EXT


def iter_roi_detections(folder_path: Path):
    """
    Генератор результатов детекции для папки.
    """
    for image_path in sorted(folder_path.iterdir()):

        if not image_path.is_file():
            continue

        if not is_supported_file(image_path):
            continue

        yield roi_detection_image(image_path)