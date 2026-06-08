from PySide6.QtWidgets import QWidget, QLabel, QMessageBox, QPushButton, QHBoxLayout
from PySide6.QtGui import QDesktopServices, QIcon, QPixmap
from PySide6.QtCore import Qt, QPoint
import qtawesome as qta
from pathlib import Path
from DataManager.DatabaseManager import DatabaseManager

class Attachment(QWidget):
    def __init__(self, filePath: str, artifactId: int, dbManager: DatabaseManager, isTemplate: bool = False):
        super().__init__()
        self.filePath: str = filePath
        self.artifactId: int = artifactId
        self.dbManager: DatabaseManager = dbManager
        self.isTemplate: bool = isTemplate

        self.iconLabel = QLabel()
        self.iconLabel.setPixmap(qta.icon("mdi.paperclip").pixmap(24, 24))
        self.fileName = QLabel(filePath.split("/")[-1])
        self.deleteButton = QPushButton("")
        self.deleteButton.setIcon(qta.icon("fa6s.xmark", color="white"))
        self.deleteButton.setProperty("class", "rounded-button red-button")
        self.deleteButton.clicked.connect(self.deleteAttachment)

        self.layout = QHBoxLayout()
        self.layout.addWidget(self.iconLabel)
        self.layout.addWidget(self.fileName)
        self.layout.addWidget(self.deleteButton)
        self.layout.setContentsMargins(5, 5, 5, 5)
        self.layout.setSpacing(5)
        self.setLayout(self.layout)
        self.setAttribute(Qt.WA_StyledBackground)
        self.setProperty("class", "content-box")

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

    def deleteAttachment(self):
        if self.artifactId is None:
            QMessageBox.warning(self, "Error", "Cannot delete: Missing artifact ID.")
            return

        _, success = self.dbManager.executeQuery(
            "DELETE FROM Artifact WHERE id = ?",
            [self.artifactId]
        )
        
        if success:
            self.parent().deleteLater()
        else:
            QMessageBox.warning(self, "Error", "Failed to delete attachment from database.")
