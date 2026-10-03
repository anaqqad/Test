#!/usr/bin/env python3
"""Flag beats whose picture is still empty some time after the cut (QC for "grey screen" gaps).

    python3 scripts/check_blank.py STILLS_DIR

STILLS_DIR holds one still per beat rendered at startFrame + 45 (1.5 s in). A frame counts as
blank when almost no pixels differ sharply from a blurred copy of the frame: the soft
background textures score 0-0.1 %, any text, line or shape scores 1.5 % or more.
"""

from __future__ import annotations

import sys
from pathlib import Path

import cv2
import numpy as np

THRESHOLD = 0.5  # percent of pixels with sharp detail


def coverage(img: np.ndarray) -> float:
    gray = cv2.cvtColor(cv2.resize(img, (960, 540)), cv2.COLOR_BGR2GRAY).astype(np.float32)
    return float(np.mean(np.abs(gray - cv2.GaussianBlur(gray, (0, 0), 6)) > 18) * 100)


def main() -> None:
    stills = sorted(Path(sys.argv[1]).glob("*.jpg"))
    scores = [(p.name, round(coverage(cv2.imread(str(p))), 2)) for p in stills]
    bad = [s for s in scores if s[1] < THRESHOLD]
    print(f"{len(bad)} of {len(stills)} beats look empty at 1.5 s (detail < {THRESHOLD} %):")
    for name, c in bad:
        print(f"  {name}  detail {c} %")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
