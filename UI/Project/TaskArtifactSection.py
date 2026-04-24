from PySide6.QtWidgets import QWidget
from typing import List

class TaskArtifactSection(QWidget):
    def __init__(self, filePaths: List[str], templates: bool = False):
        super().__init__()