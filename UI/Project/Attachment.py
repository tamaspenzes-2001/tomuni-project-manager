from PySide6.QtWidgets import QWidget, QLabel, QMessageBox, QPushButton, QHBoxLayout
from PySide6.QtGui import QDesktopServices, QIcon, QPixmap
from PySide6.QtCore import Qt, QPoint
import qtawesome as qta
from pathlib import Path

class Attachment(QWidget):
    def __init__(self, filePath: str):
        super().__init__()
        self.filePath = filePath

        self.iconLabel = QLabel()
        self.iconLabel.setPixmap(qta.icon("mdi.paperclip").pixmap(24, 24))
        self.fileName = QLabel(filePath.split("/")[-1])
        self.deleteButton = QPushButton("x")
        self.deleteButton.clicked.connect(self.deleteLater)

        self.layout = QHBoxLayout()
        self.layout.addWidget(self.iconLabel)
        self.layout.addWidget(self.fileName)
        self.layout.addWidget(self.deleteButton)
        self.setLayout(self.layout)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            pos: QPoint = event.position().toPoint()
            if self.deleteButton.geometry().contains(pos):
                return
            self.openFile()
        super().mousePressEvent(event)

    def openFile(self):
        path = Path(self.filePath)
        if not path.exists():
            QMessageBox.critical(self, "Error", f"File not found:\n{self.filePath}")
            return
        url: str = path.as_uri()
        if not QDesktopServices.openUrl(url):
            QMessageBox.critical(self, "Error", "Could not open the file.")