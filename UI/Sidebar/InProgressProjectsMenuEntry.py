from PySide6.QtWidgets import QWidget, QLabel, QHBoxLayout

class InProgressProjectsMenuEntry(QWidget):
    def __init__(self, name):
        super().__init__()
        print("Hello")
        self.name = QLabel(name)
        self.layout = QHBoxLayout()
        self.layout.addWidget(self.name)
        self.setLayout(self.layout)