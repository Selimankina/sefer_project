from src.preprocessing.process_folder import process_preprocessing
from .process_image import process_image


def process_digit_detection(folder_path):
    for preprocess in process_preprocessing(folder_path):
        yield process_image(preprocess)