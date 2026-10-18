"""Make the repo's scripts importable.

The repo is not a package: modules live at the root, in operators/, code/integration/,
and stellar_structure/ (whose files import each other as flat top-level names).
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
for sub in ("", "operators", "code/integration", "stellar_structure"):
    p = str(ROOT / sub)
    if p not in sys.path:
        sys.path.insert(0, p)
