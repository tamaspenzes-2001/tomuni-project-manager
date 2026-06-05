from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from typing import Dict, List
from PySide6.QtCore import Qt
from UI.Project.TaskHeader import TaskHeader
from UI.Project.TaskArtifactSection import TaskArtifactSection
from DataManager.DatabaseManager import DatabaseManager
from DataManager.ConfigManager import ConfigManager

class Task(QWidget):
    def __init__(self, taskData: Dict, dbManager: DatabaseManager, confManager: ConfigManager, isSubtask: bool = False):
        super().__init__()
        self.taskData: Dict = taskData

        self.header = TaskHeader(taskData, dbManager, confManager)
        self.description = QLabel(taskData["description"])
        self.description.setContentsMargins(10, 0, 0, 0)
        self.description.setTextFormat(Qt.MarkdownText)
        self.description.setProperty("class", "")
        self.description.setVisible(False)
        self.artifactTemplates = TaskArtifactSection(
            taskData["id"], taskData["artifactTemplates"], dbManager, templates=True
        )
        self.artifactTemplates.setVisible(False)
        self.artifacts = TaskArtifactSection(taskData["id"], taskData["artifacts"], dbManager)
        self.artifacts.setVisible(False)

        self.taskBodyLayout = QVBoxLayout()
        self.taskBodyLayout.addWidget(self.description)
        self.taskBodyLayout.addWidget(self.artifactTemplates)
        self.taskBodyLayout.addWidget(self.artifacts)
        self.taskBodyLayout.setContentsMargins(30, 0, 0, 0)
        
        self.subtasks: List[Task] = [Task(subtask, dbManager, confManager, isSubtask=True) for subtask in taskData["subtasks"]]
        for subtask in self.subtasks:
            subtask.setVisible(False)
            subtask.setProperty("class", "top-border")
            self.taskBodyLayout.addWidget(subtask)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.header)
        self.layout.addLayout(self.taskBodyLayout)

        self.setLayout(self.layout)
        self.setAttribute(Qt.WA_StyledBackground)
        classValue: str = "top-border" if isSubtask else "bottom-border"
        self.setProperty("class", classValue)

        self.updateGeometry()
        self.update()
        if self.parent():
            self.parent().updateGeometry()
            self.parent().update()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        for subtask in self.subtasks:
            subtask.updateGeometry()