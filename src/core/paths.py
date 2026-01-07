from __future__ import annotations

from pathlib import Path


def ensure_output_dirs(base: str | Path = "outputs") -> dict[str, Path]:
    """Ensure output directories exist and return their Paths."""
    base = Path(base)
    tables = base / "tables"
    figures = base / "figures"
    tables.mkdir(parents=True, exist_ok=True)
    figures.mkdir(parents=True, exist_ok=True)
    return {"base": base, "tables": tables, "figures": figures}
