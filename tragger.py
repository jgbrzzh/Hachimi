import src.MainProcess
import sys


import os
from pathlib import Path
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))
os.chdir(Path(__file__).resolve().parent / "src") #切换工作目录到src 无奈之举


src.MainProcess.main()

