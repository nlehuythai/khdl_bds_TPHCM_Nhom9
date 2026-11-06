from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "src" / "UI" / "app.py"

if __name__ == "__main__":
    subprocess.run(
        [sys.executable, "-m", "streamlit", "run", str(APP)],
        cwd=ROOT,
        check=True,
    )
