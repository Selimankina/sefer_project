from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from pathlib import Path

import numpy as np

from src.pipeline.status import PipelineStatus


@dataclass
class PipelineState:
    # --- input ---
    image_path: Path
    image: Optional[np.ndarray] = None

    # --- roi ---
    roi: Optional[np.ndarray] = None

    # --- preprocessing ---
    processed_image: Optional[np.ndarray] = None
    preprocessing_meta: Dict[str, Any] = field(default_factory=dict)

    # --- digits ---
    digits: List = field(default_factory=list)

    # --- result ---
    number: Optional[str] = None
    confidence: Optional[float] = None

    # --- renaming ---
    new_name: Optional[str] = None
    renamed_path: Optional[Path] = None
    should_mark_unreliable: bool = False

    # --- pipeline control ---
    status: PipelineStatus = PipelineStatus.INIT
    error_stage: Optional[str] = None
    error_message: Optional[str] = None