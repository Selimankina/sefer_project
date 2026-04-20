from ultralytics import YOLO
import numpy as np

from config import MODELS_DIR
from src.common.schemas import ROI

model = YOLO(MODELS_DIR / "roi_detector.pt")


def detect_rois(image: np.ndarray) -> list[ROI]:
    """
        Детектирует области интереса (ROI) на изображении с помощью YOLO.

        Для каждой найденной области возвращает:
        - bounding box (bbox)
        - confidence
        - keypoints (если доступны)

        Args:
            image (np.ndarray): Входное изображение.

        Returns:
            list[ROI]: Список найденных ROI (может быть пустым).
        """
    results = model(image, verbose=False)
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

        rois.append(
            ROI(
                bbox=bbox,
                confidence=conf,
                keypoints=keypoints,
            )
        )

    return rois