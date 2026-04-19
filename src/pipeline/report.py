import csv
from pathlib import Path
from typing import List

from src.pipeline.state import PipelineState, PipelineStatus


def save_csv_report(states: List[PipelineState], output_dir: Path):
    output_dir.mkdir(parents=True, exist_ok=True)

    report_path = output_dir / "report.csv"

    # --- summary ---
    total = len(states)
    renamed = 0
    low_conf = 0
    failed = 0

    for s in states:
        if s.status == PipelineStatus.OK:
            renamed += 1

        elif s.status == PipelineStatus.LOW_CONFIDENCE:
            renamed += 1
            low_conf += 1

        else:
            failed += 1

    # --- сортировка ---
    def sort_key(s: PipelineState):
        if s.new_name:
            return s.new_name
        return s.image_path.name

    sorted_states = sorted(states, key=sort_key)

    # --- запись ---
    with open(report_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        # =========================
        # SUMMARY
        # =========================
        writer.writerow([f"Всего файлов: {total}"])
        writer.writerow([f"Переименовано: {renamed}"])
        writer.writerow([f"Низкая уверенность: {low_conf}"])
        writer.writerow([f"Не переименовано: {failed}"])

        writer.writerow([])  # пустая строка

        # =========================
        # TABLE
        # =========================
        writer.writerow([
            "old_name",
            "new_name",
            "status",
            "confidence",
            "error_stage",
        ])

        for s in sorted_states:
            writer.writerow([
                s.image_path.name,
                getattr(s, "new_name", None),
                s.status.value,
                s.confidence,
                s.error_stage,
            ])

    return report_path