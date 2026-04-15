from src.roi_detection.process_folder import iter_roi_detections
from src.preprocessing.process_image import process_image


def process_preprocessing(folder_path):
    for detection in iter_roi_detections(folder_path):
        yield process_image(detection)