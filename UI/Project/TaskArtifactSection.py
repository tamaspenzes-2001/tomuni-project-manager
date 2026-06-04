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
                idMap: Dict = {}
                while query.next():
                    idMap[query.value("filePath")] = query.value("id")
                
                for path in filePaths:
                    artifactId = idMap.get(path)
                    attachment = Attachment(path, artifactId, dbManager, templates)

                    # --- NEW WRAPPER LOGIC ---
                    wrapper = QWidget()
                    wrapper_layout = QHBoxLayout(wrapper)
                    wrapper_layout.setContentsMargins(0, 7, 7, 0) # Internal padding creates the gap
                    wrapper_layout.setSpacing(0)
                    wrapper_layout.addWidget(attachment)
                    wrapper_layout.addStretch() # Optional: helps alignment
                    # -------------------------

                    self.attachmentsLayout.addWidget(wrapper)
        self.button_wrapper = QWidget()
        button_layout = QHBoxLayout(self.button_wrapper)
        button_layout.setContentsMargins(0, 7, 7, 0)
        button_layout.setSpacing(0)
        button_layout.addWidget(self.addAttachmentButton)
        button_layout.addStretch()
        
        self.attachmentsLayout.addWidget(self.button_wrapper)
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
            self.attachmentsLayout.removeWidget(self.button_wrapper)
            
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
                wrapper_layout = QHBoxLayout(wrapper)
                wrapper_layout.setContentsMargins(0, 7, 7, 0) # Internal padding creates the gap
                wrapper_layout.setSpacing(0)
                wrapper_layout.addWidget(newAttachment)
                wrapper_layout.addStretch()
                
                self.attachmentsLayout.addWidget(wrapper)
                self.attachmentsLayout.addWidget(self.button_wrapper)
                self.filePaths.append(fileName)