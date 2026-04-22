from PySide6.QtWidgets import QWidget, QLabel, QHBoxLayout

class FinishedProjectsTab(QWidget):
    def __init__(self, name):
        super().__init__()
        self.name = QLabel(name)
        self.layout = QHBoxLayout()
        self.layout.addWidget(self.name)
        self.setLayout(self.layout)

    def openProject(self):
        pass