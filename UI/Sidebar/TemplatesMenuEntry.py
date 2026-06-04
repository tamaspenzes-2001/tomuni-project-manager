from PySide6.QtWidgets import QWidget, QLabel, QPushButton, QHBoxLayout, QSizePolicy
from PySide6.QtCore import Qt
import qtawesome as qta

class TemplatesMenuEntry(QWidget):
    def __init__(self, text):
        super().__init__()
        self.name = QLabel(text)
        self.deleteButton = QPushButton()
        self.deleteButton.setIcon(qta.icon("ri.delete-bin-6-line"))
        self.deleteButton.clicked.connect(self.deleteTemplate)
        self.deleteButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.deleteButton.setProperty("class", "button red-button")

        self.layout = QHBoxLayout()
        self.layout.addWidget(self.name)
        self.layout.addWidget(self.deleteButton)
        self.layout.setSpacing(0)
        self.setLayout(self.layout)

        self.mouseReleaseEvent=self.openTemplate
        self.setAttribute(Qt.WA_StyledBackground)
        self.setProperty("class", "bottom-border")

    def openTemplate(self, event):
        pass

    def deleteTemplate(self):
        self.sender().parent().deleteLater()