from PySide6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout
from superqt import QFlowLayout
from typing import List
from UI.Project.Attachment import Attachment

class TaskArtifactSection(QWidget):
    def __init__(self, filePaths: List[str], templates: bool = False):
        super().__init__()
        self.label = QLabel("Artifact templates" if templates else "Artifacts")
        self.labelLayout = QVBoxLayout()
        self.labelLayout.addWidget(self.label)
        self.labelLayout.addStretch()

        self.addAttachmentButton = QPushButton("+")
        self.addAttachmentButton.clicked.connect(self.addAttachment)
        self.attachmentsLayout = QFlowLayout()
        for path in filePaths:
            self.attachmentsLayout.addWidget(Attachment(path))
        self.attachmentsLayout.addWidget(self.addAttachmentButton)
        
        self.layout = QHBoxLayout()
        self.layout.addLayout(self.labelLayout)
        self.layout.addLayout(self.attachmentsLayout)
        self.layout.addStretch()
        self.setLayout(self.layout)

    def addAttachment(self):
        pass