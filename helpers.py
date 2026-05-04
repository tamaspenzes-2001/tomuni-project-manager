import os

def assetPath(relativePath):
    tempDir: str = os.getenv("NUITKA_TEMP_DIR")
    if tempDir:
        basePath: str = os.path.join(tempDir, "assets")
    else:
        basePath: str = os.path.join(os.path.abspath(os.path.dirname(__file__)), "assets")
    return os.path.join(basePath, relativePath)

def dataPath(fileName):
    filePath: str = os.path.expanduser(f"~/.config/TomUni/{fileName}")
    os.makedirs(os.path.dirname(filePath), exist_ok=True)
    return filePath
