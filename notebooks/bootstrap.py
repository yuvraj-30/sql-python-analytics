"""Repository bootstrap for notebooks and ad-hoc execution.

This module ensures the repository root (the directory containing 'src/') is added
to sys.path so that imports like `from src...` work reliably when running
notebooks from the /notebooks folder (or any subfolder inside the repo).
"""

from pathlib import Path
import sys

# notebooks/ is expected to be one level below the repository root
REPO_ROOT = Path(__file__).resolve().parents[1]

repo_root_str = str(REPO_ROOT)
if repo_root_str not in sys.path:
    sys.path.insert(0, repo_root_str)
