import os
from pathlib import Path

# Directories for data and reports
DATA_ROOT = Path(os.getenv("DATA_ROOT", "./data"))
REPORTS_DIR = Path("./reports")
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

