"""Generate synthetic data placeholders for local development."""
from __future__ import annotations

from pathlib import Path

from configs.paths import SYNTHETIC_DATA_DIR


def main() -> None:
    SYNTHETIC_DATA_DIR.mkdir(parents=True, exist_ok=True)
    output_path = SYNTHETIC_DATA_DIR / "synthetic_data.json"
    output_path.write_text('{"samples": 0}\n', encoding="utf-8")
    print(f"Created {output_path}")


if __name__ == "__main__":
    main()
