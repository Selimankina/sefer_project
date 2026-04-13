from src.preprocessing.schemas import PreprocessResult, PreprocessStatus
from .detector import detect_digits
from .schemas import DigitDetectionResult, DigitDetectionStatus


def process_image(preprocess: PreprocessResult) -> DigitDetectionResult:
    image_path = preprocess.image_path

    # --- проверка статуса препроцессинга ---
    if preprocess.status != PreprocessStatus.OK and preprocess.status != PreprocessStatus.FALLBACK:
        return DigitDetectionResult(
            image_path=image_path,
            status=DigitDetectionStatus.ERROR,
            roi=None,
            error_message=f"invalid_preprocess_status: {preprocess.status.value}"
        )

    roi = preprocess.roi

    if roi is None:
        return DigitDetectionResult(
            image_path=image_path,
            status=DigitDetectionStatus.ERROR,
            roi=None,
            error_message="roi_is_none"
        )

    # --- запуск детекции ---
    return detect_digits(image_path, roi)