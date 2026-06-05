from PySide6.QtWidgets import QWidget, QLabel, QPushButton, QFileDialog, QSizePolicy, QVBoxLayout, QHBoxLayout
from superqt import QFlowLayout
import qtawesome as qta
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

        self.addAttachmentButton = QPushButton("")
        self.addAttachmentButton.setIcon(qta.icon("ri.add-fill"))
        self.addAttachmentButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.addAttachmentButton.setProperty("class", "button green-button")
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
                idMap: Dict[str, int] = {}
                while query.next():
                    idMap[query.value("filePath")] = query.value("id")
                
                for path in filePaths:
                    artifactId: int = idMap.get(path)
                    attachment = Attachment(path, artifactId, dbManager, templates)

                    wrapper = QWidget()
                    wrapperLayout = QHBoxLayout(wrapper)
                    wrapperLayout.setContentsMargins(0, 7, 7, 0)
                    wrapperLayout.setSpacing(0)
                    wrapperLayout.addWidget(attachment)
                    wrapperLayout.addStretch()

                    self.attachmentsLayout.addWidget(wrapper)
        self.buttonWrapper = QWidget()
        buttonLayout = QHBoxLayout(self.buttonWrapper)
        buttonLayout.setContentsMargins(0, 7, 7, 0)
        buttonLayout.setSpacing(0)
        buttonLayout.addWidget(self.addAttachmentButton)
        buttonLayout.addStretch()
        
        self.attachmentsLayout.addWidget(self.buttonWrapper)
        self.attachmentsLayout.setContentsMargins(2, 2, 2, 2)
        self.attachmentsLayout.setSpacing(15)
        
        self.layout = QHBoxLayout()
        self.layout.addLayout(self.labelLayout)
        self.layout.addLayout(self.attachmentsLayout)
        self.layout.addStretch()
        self.setLayout(self.layout)

    def addAttachment(self):
        fileName, fileChosen = QFileDialog.getOpenFileName(self)
        if fileChosen:
            self.attachmentsLayout.removeWidget(self.buttonWrapper)
            
            _, success = self.dbManager.executeQuery(
                "INSERT INTO Artifact (filePath, template, taskId) VALUES (?, ?, ?)",
                [fileName, self.templates, self.id]
            )
            
            if success:
                query, _ = self.dbManager.executeQuery("SELECT last_insert_rowid()")
                query.next()
                newId = query.value(0)

                newAttachment = Attachment(fileName, newId, self.dbManager, self.templates)

                wrapper = QWidget()
                wrapperLayout = QHBoxLayout(wrapper)
                wrapperLayout.setContentsMargins(0, 7, 7, 0)
                wrapperLayout.setSpacing(0)
                wrapperLayout.addWidget(newAttachment)
                wrapperLayout.addStretch()
                
                self.attachmentsLayout.addWidget(wrapper)
                self.attachmentsLayout.addWidget(self.buttonWrapper)
                self.filePaths.append(fileName)