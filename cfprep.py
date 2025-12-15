#!/usr/bin/env python3

from __future__ import annotations

import runpy
import sys
from pathlib import Path


def main() -> None:
    repo_root = Path(__file__).resolve().parent
    codeforces_dir = repo_root / "codeforces"
    target = codeforces_dir / "cfprep.py"

    argv = sys.argv[1:]
    if argv[:1] == ["get"] and "--root" not in argv:
        argv = ["get", "--root", str(codeforces_dir)] + argv[1:]

    sys.argv = [str(target)] + argv
    runpy.run_path(str(target), run_name="__main__")


if __name__ == "__main__":
    main()
