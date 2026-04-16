from PySide6.QtWidgets import QWidget, QLabel, QPushButton, QHBoxLayout
import qtawesome as qta

class TemplatesMenuEntry(QWidget):
    def __init__(self, text):
        super().__init__()
        self.name = QLabel(text)
        self.deleteButton = QPushButton()
        self.deleteButton.setIcon(qta.icon("ri.delete-bin-6-line"))

        self.layout = QHBoxLayout()
        self.layout.addWidget(self.name)
        self.layout.addWidget(self.deleteButton)
        self.setLayout(self.layout)

        self.mouseReleaseEvent=self.openTemplate
        self.deleteButton.clicked.connect(self.deleteTemplate)

    def openTemplate(self, event):
        pass

    def deleteTemplate(self):
        self.sender().parent().deleteLater()