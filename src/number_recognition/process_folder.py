from src.digits_detection.process_folder import process_digit_detection
from .process_image import process_image


def process_number_recognition(folder_path):
    for detection in process_digit_detection(folder_path):
        yield process_image(detection)