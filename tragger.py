import src.MainProcess
import sys
from pathlib import Path

sys.path[0] = str(Path(sys.path[0]) / "src")
src.MainProcess.main()

