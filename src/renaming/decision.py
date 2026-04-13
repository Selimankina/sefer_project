from .schemas import FinalStatus
from src.number_recognition.schemas import NumberStatus

def decide(number_result) -> FinalStatus:
    status = number_result.status

    if status == NumberStatus.OK:
        return FinalStatus.OK

    if status == NumberStatus.LOW_CONFIDENCE:
        return FinalStatus.LOW_CONFIDENCE

    return FinalStatus.FAILED