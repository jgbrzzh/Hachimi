import sys
import os
def Encode():
    sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
    import GetFilepath.GetFile as GetFile
    import Config.Config as Config
    GetFile.