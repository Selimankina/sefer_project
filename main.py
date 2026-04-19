import argparse
from pathlib import Path

from tqdm import tqdm

from src.pipeline.process_folder import process_folder
from src.pipeline.report import save_csv_report


def main():
    """
        Точка входа в приложение.

        Выполняет:
        - чтение аргументов командной строки;
        - проверку входной папки;
        - запуск пайплайна обработки изображений;
        - сбор результатов;
        - генерацию CSV-отчёта.
        """
    parser = argparse.ArgumentParser(
        description="Rename photos and generate report"
    )

    parser.add_argument(
        "input_dir",
        type=str,
        help="Path to folder with images",
    )

    args = parser.parse_args()
    input_dir = Path(args.input_dir)

    if not input_dir.exists():
        print(f"Folder not found: {input_dir}")
        return

    print(f"Processing folder: {input_dir}\n")

    files = [p for p in input_dir.glob("*") if p.is_file()]

    states = []

    for state in tqdm(
        process_folder(input_dir),
        total=len(files),
        desc="Processing",
    ):
        states.append(state)

    # --- отчёт ---
    save_csv_report(states, input_dir)

    print("\nDone!")
    print(f"Processed {len(states)} files")


if __name__ == "__main__":
    main()