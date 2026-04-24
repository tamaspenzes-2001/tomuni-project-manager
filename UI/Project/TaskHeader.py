from PySide6.QtWidgets import QWidget
from typing import Dict

class TaskHeader(QWidget):
    def __init__(self, taskData: Dict):
        super().__init__()