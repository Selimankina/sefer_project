from pathlib import Path

# корень проекта
BASE_DIR = Path(__file__).resolve().parents[1]

# папки
DATA_DIR = BASE_DIR / 'data'
SRC_DIR = BASE_DIR / 'src'
MODELS_DIR = BASE_DIR / 'models'