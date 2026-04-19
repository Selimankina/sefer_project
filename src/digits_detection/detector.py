import numpy as np
import traceback
from ultralytics import YOLO

from config import MODELS_DIR
from src.common.schemas import Digit

model = YOLO(MODELS_DIR / "digit_detector.pt")


def detect_digits(image: np.ndarray) -> list[Digit] | None:
    """
    Детектирует цифры на изображении с помощью YOLO-модели.

    Выполняет предсказание, извлекает bounding boxes и формирует
    список объектов Digit.

    Args:
        image (np.ndarray): Входное изображение в формате numpy-массива.

    Returns:
        list[Digit] | None:
            - список найденных цифр (может быть пустым, если ничего не найдено);
            - None, если произошла ошибка или изображение некорректно.

    Notes:
        - Максимум детекций ограничен (max_det=5).
        - Используется CPU для инференса.
    """

    try:
        if image is None:
            return None

        results = model.predict(
            image,
            max_det=5,
            device="cpu"
        )

        result = results[0]
        boxes = result.boxes

        if boxes is None or len(boxes) == 0:
            return []

        digits = []

        for box in boxes:
            cls_id = int(box.cls[0])
            label = model.names[cls_id]
            conf = float(box.conf[0])

            x1, y1, x2, y2 = box.xyxy[0].tolist()

            bbox = np.array([
                [x1, y1],
                [x2, y1],
                [x2, y2],
                [x1, y2]
            ], dtype="float32")

            digits.append(
                Digit(
                    bbox=bbox,
                    label=label,
                    confidence=conf
                )
            )

        return digits

    except Exception:
        print(traceback.format_exc())
        return None