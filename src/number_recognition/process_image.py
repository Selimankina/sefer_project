from src.digits_detection.schemas import DigitDetectionResult, DigitDetectionStatus

from src.number_recognition.schemas import NumberResult, NumberStatus
from src.number_recognition.assembler import assemble_number
from src.number_recognition.formatter import format_number


LOW_CONF_THRESHOLD = 0.96


def process_image(detection: DigitDetectionResult) -> NumberResult:
    image_path = detection.image_path

    if detection.status not in (
        DigitDetectionStatus.OK,
        DigitDetectionStatus.LOW_CONFIDENCE,
    ):
        return NumberResult(
            image_path=image_path,
            status=NumberStatus.ERROR,
            raw_number=None,
            formatted_number=None,
            confidence=None,
            digits=detection.digits,
            error_message=f"invalid_digit_status: {detection.status.value}"
        )

    raw_number, confidence, error = assemble_number(detection.digits)

    if error == "no_digits":
        status = NumberStatus.NO_NUMBER

    elif error == "low_confidence":
        status = NumberStatus.LOW_CONFIDENCE

    elif error == "invalid_format":
        status = NumberStatus.INVALID_FORMAT

    elif error is not None:
        status = NumberStatus.ERROR

    else:
        if confidence < LOW_CONF_THRESHOLD:
            status = NumberStatus.LOW_CONFIDENCE
        else:
            status = NumberStatus.OK

    formatted = format_number(raw_number) if raw_number else None

    return NumberResult(
        image_path=image_path,
        status=status,
        raw_number=raw_number,
        formatted_number=formatted,
        confidence=confidence,
        digits=detection.digits,
        error_message=error
    )