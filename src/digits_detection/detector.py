import numpy as np
from ultralytics import YOLO
from config import MODELS_DIR

from .schemas import Digit, DigitDetectionResult, DigitDetectionStatus

model = YOLO(MODELS_DIR / 'digit_detector.pt')

def detect_digits(image_path, roi) -> DigitDetectionResult:
    try:
        if roi is None:
            return DigitDetectionResult(
                image_path=image_path,
                status=DigitDetectionStatus.ERROR,
                roi=None,
                error_message="roi_is_none"
            )

        results = model.predict(
            roi,
            max_det=5,
            device="cpu"
        )

        result = results[0]
        boxes = result.boxes

        if boxes is None or len(boxes) == 0:
            return DigitDetectionResult(
                image_path=image_path,
                status=DigitDetectionStatus.NO_DIGITS,
                roi=roi,
                digits=[]
            )

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

        # --- статус ---
        if not digits:
            status = DigitDetectionStatus.NO_DIGITS

        elif len(digits) > 6:
            status = DigitDetectionStatus.TOO_MANY_DIGITS

        elif all(d.confidence < 0.5 for d in digits):
            status = DigitDetectionStatus.LOW_CONFIDENCE

        else:
            status = DigitDetectionStatus.OK

        return DigitDetectionResult(
            image_path=image_path,
            status=status,
            roi=roi,
            digits=digits
        )

    except Exception as e:
        import traceback

        return DigitDetectionResult(
            image_path=image_path,
            status=DigitDetectionStatus.ERROR,
            roi=roi,
            error_message=f"{e}\n{traceback.format_exc()}"
        )