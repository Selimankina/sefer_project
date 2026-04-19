import cv2
import numpy as np
from pathlib import Path
import rawpy


RAW_EXTENSIONS = {".cr2", ".nef", ".arw", ".dng"}
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".tiff", ".bmp"}


def load_image(path: Path) -> np.ndarray | None:
    """
        Загружает изображение из файла.

        Поддерживает:
        - RAW форматы (через rawpy)
        - обычные изображения (через OpenCV)

        Args:
            path (Path): Путь к файлу изображения.

        Returns:
            np.ndarray | None: Изображение в формате BGR или None,
            если файл не поддерживается или не удалось загрузить.

        Notes:
            - RAW изображения конвертируются в RGB, затем в BGR.
            - Неподдерживаемые форматы игнорируются.
        """
    try:
        suffix = path.suffix.lower()

        # --- RAW ---
        if suffix in RAW_EXTENSIONS:
            with rawpy.imread(str(path)) as raw:
                rgb = raw.postprocess()
                if rgb is None:
                    return None
                return cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)

        # --- обычные изображения ---
        if suffix in IMAGE_EXTENSIONS:
            image = cv2.imread(str(path))
            if image is None:
                return None
            return image

        # --- всё остальное ---
        return None

    except Exception:
        return None