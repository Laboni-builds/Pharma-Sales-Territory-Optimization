"""Re-export from data/ for clean imports within src/."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "data"))
from generate_synthetic_data import generate_zip_data  # noqa: E402, F401
