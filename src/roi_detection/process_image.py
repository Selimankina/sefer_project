from pathlib import Path
import traceback
from src.roi_detection.detector import detect_rois
from src.roi_detection.schemas import DetectionResult, DetectionStatus

def roi_detection_image(image_path: Path) -> DetectionResult:
    """
    Обрабатывает одно изображение.
    Выбирает лучшую табличку.
    """
    try:
        rois = detect_rois(image_path)

        if not rois:
            return DetectionResult(
                image_path=image_path,
                status=DetectionStatus.NO_PLATE,
                rois=[]
            )

        best_roi = max(rois, key=lambda r: r.confidence)

        status = (
            DetectionStatus.OK
            if len(rois) == 1
            else DetectionStatus.MULTIPLE_PLATES
        )

        return DetectionResult(
            image_path=image_path,
            status=status,
            best_roi=best_roi
        )


    except Exception as e:
        error_message = (
            f"Error ROI detecting {image_path}:\n"
            f"{traceback.format_exc()}"
        )

        return DetectionResult(
            image_path=image_path,
            status=DetectionStatus.ERROR,
            error_message=error_message
        )