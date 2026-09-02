"""Start the Phase 1 backend from the repository root."""

import subprocess
import sys
from pathlib import Path

backend = Path(__file__).resolve().parents[1] / "backend"
subprocess.run([sys.executable, "-m", "uvicorn", "app.main:app", "--reload"], cwd=backend, check=True)
