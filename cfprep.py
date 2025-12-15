#!/usr/bin/env python3

from __future__ import annotations

import runpy
import os
from pathlib import Path


def main() -> None:
    repo_root = Path(__file__).resolve().parent
    codeforces_dir = repo_root / "codeforces"
    os.chdir(codeforces_dir)
    runpy.run_path(str(codeforces_dir / "cfprep.py"), run_name="__main__")


if __name__ == "__main__":
    main()
