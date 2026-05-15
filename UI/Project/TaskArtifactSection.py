from PySide6.QtWidgets import QWidget, QLabel, QPushButton, QFileDialog, QVBoxLayout, QHBoxLayout
from superqt import QFlowLayout
from typing import List
from UI.Project.Attachment import Attachment
from DataManager.DatabaseManager import DatabaseManager

class TaskArtifactSection(QWidget):
    def __init__(self, taskId: int, filePaths: List[str], dbManager: DatabaseManager, templates: bool = False):
        super().__init__()
        self.id: int = taskId
        self.filePaths: List[str] = filePaths
        self.dbManager: DatabaseManager = dbManager
        self.templates: bool = templates

        self.label = QLabel("Artifact templates" if templates else "Artifacts")
        self.labelLayout = QVBoxLayout()
        self.labelLayout.addWidget(self.label)
        self.labelLayout.addStretch()

        self.addAttachmentButton = QPushButton("+")
        self.addAttachmentButton.clicked.connect(self.addAttachment)
        self.attachmentsLayout = QFlowLayout()
        if filePaths:
            placeholders: str = ",".join(["?"] * len(filePaths))
            queryStr: str = f"""
            SELECT id, filePath FROM Artifact 
            WHERE taskId = ? AND template = ? AND filePath IN ({placeholders})
            """
            query, success = self.dbManager.executeQuery(queryStr, [taskId, templates] + filePaths)
            
            if success:
                idMap: Dict = {}
                while query.next():
                    idMap[query.value("filePath")] = query.value("id")
                
                for path in filePaths:
                    artifactId = idMap.get(path)
                    self.attachmentsLayout.addWidget(Attachment(path, artifactId, dbManager, templates))
        self.attachmentsLayout.addWidget(self.addAttachmentButton)
        
        self.layout = QHBoxLayout()
        self.layout.addLayout(self.labelLayout)
        self.layout.addLayout(self.attachmentsLayout)
        self.layout.addStretch()
        self.setLayout(self.layout)

    def addAttachment(self):
        fileName, fileChosen = QFileDialog.getOpenFileName(self)
        if fileChosen:
            self.attachmentsLayout.removeWidget(self.addAttachmentButton)
            
            _, success = self.dbManager.executeQuery(
                "INSERT INTO Artifact (filePath, template, taskId) VALUES (?, ?, ?)",
                [fileName, self.templates, self.id]
            )
            
            if success:
                query, _ = self.dbManager.executeQuery("SELECT last_insert_rowid()")
                query.next()
                newId = query.value(0)
                
                self.attachmentsLayout.addWidget(Attachment(fileName, newId, self.dbManager, self.templates))
                self.attachmentsLayout.addWidget(self.addAttachmentButton)
                self.filePaths.append(fileName)