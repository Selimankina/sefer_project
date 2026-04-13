from pathlib import Path
from ultralytics import YOLO

from config import MODELS_DIR
from src.roi_detection.schemas import ROI

model = YOLO(MODELS_DIR / 'roi_detector.pt')

def detect_rois(image_path: Path) -> list[ROI]:
    """
    Детекция табличек на изображении.

    Args:
        image_path (Path)

    Returns:
        list[ROI]: список найденных табличек (может быть пустым)
    """
    results = model(image_path)
    result = results[0]

    boxes_obj = result.boxes
    keypoints_obj = result.keypoints

    if boxes_obj is None or len(boxes_obj) == 0:
        return []

    boxes = boxes_obj.xyxy.cpu().numpy()
    confs = boxes_obj.conf.cpu().numpy()

    rois = []

    for i in range(len(boxes)):
        bbox = [int(round(x)) for x in boxes[i]]
        conf = float(confs[i])

        keypoints = None

        if keypoints_obj is not None and len(keypoints_obj.xy) > i:
            kpts_xy = keypoints_obj.xy[i].cpu().numpy()
            kpts_conf = keypoints_obj.conf[i].cpu().numpy()

            keypoints = [
                [int(round(x)), int(round(y)), float(c)]
                for (x, y), c in zip(kpts_xy, kpts_conf)
            ]

        rois.append(ROI(
            bbox=bbox,
            confidence=conf,
            keypoints=keypoints
        ))

    return rois