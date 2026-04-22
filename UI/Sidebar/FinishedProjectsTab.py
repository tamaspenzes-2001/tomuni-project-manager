from PySide6.QtWidgets import QScrollArea, QWidget, QVBoxLayout

class FinishedProjectsTab(QScrollArea):
    def __init__(self):
        super().__init__()
        self.menu = QWidget()
        self.menuLayout = QVBoxLayout()
        self.menuLayout.addStretch()
        self.menu.setLayout(self.menuLayout)
        self.setWidget(self.menu)
        self.setWidgetResizable(True)