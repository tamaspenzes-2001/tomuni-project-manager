from PySide6.QtWidgets import QWidget
from typing import List, Dict

class Phase(QWidget):
    def __init__(self, phaseData: List[Dict]):
        super().__init__()
