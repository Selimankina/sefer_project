from enum import Enum


class PipelineStatus(str, Enum):
    INIT = "init"

    LOAD_ERROR = "load_error"

    NO_ROI = "no_roi"
    PREPROCESS_ERROR = "preprocess_error"
    NO_DIGITS = "no_digits"
    NO_NUMBER = "no_number"

    LOW_CONFIDENCE = "low_confidence"

    OK = "ok"