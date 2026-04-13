from dataclasses import dataclass
from enum import Enum
from pathlib import Path


class RenameStatus(Enum):
    RENAMED = "renamed"
    ERROR = "error"


@dataclass
class RenameResult:
    image_path: Path
    new_path: Path | None
    status: RenameStatus
    is_low_confidence: bool = False
    message: str | None = None