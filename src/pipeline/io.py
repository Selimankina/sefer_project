import cv2
import numpy as np
from pathlib import Path
import rawpy


RAW_EXTENSIONS = {".cr2", ".nef", ".arw", ".dng"}
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".tiff", ".bmp"}


def load_image(path: Path) -> np.ndarray | None:
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