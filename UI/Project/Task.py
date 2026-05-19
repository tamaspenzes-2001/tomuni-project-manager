from PySide6.QtWidgets import QWidget, QToolButton, QVBoxLayout, QLabel, QHBoxLayout
from PySide6.QtCore import Qt
from PySide6.QtGui import QTextDocument
import qtawesome as qta
from typing import Dict, List
from UI.Project.TaskHeader import TaskHeader
from UI.Project.TaskArtifactSection import TaskArtifactSection
from UI.Dialogs.TaskDialog import TaskDialog
from DataManager.DatabaseManager import DatabaseManager
from DataManager.ConfigManager import ConfigManager

class Task(QWidget):
    def __init__(self, taskData: Dict, dbManager: DatabaseManager, confManager: ConfigManager):
        super().__init__()
        self.taskData: Dict = taskData
        self.expanded: bool = True

        self.expandCollapseButton = QToolButton()
        self.expandCollapseButton.setIcon(qta.icon("fa5s.chevron-right"))
        self.expandCollapseButton.clicked.connect(self.expandCollapse)
        self.expandCollapseLayout = QVBoxLayout()
        self.expandCollapseLayout.addWidget(self.expandCollapseButton)
        self.expandCollapseLayout.addStretch()

        self.header = TaskHeader(taskData, dbManager, confManager)
        self.description = QLabel(taskData["description"])
        self.description.setTextFormat(Qt.MarkdownText)
        self.artifactTemplates = TaskArtifactSection(
            taskData["id"], taskData["artifactTemplates"], dbManager, templates=True
        )
        self.artifacts = TaskArtifactSection(taskData["id"], taskData["artifacts"], dbManager)

        self.subtasksLayout = QVBoxLayout()
        self.subtasks: List[Task] = [Task(subtask, dbManager, confManager) for subtask in taskData["subtasks"]]
        for subtask in self.subtasks:
            self.subtasksLayout.addWidget(subtask)

        self.taskLayout = QVBoxLayout()
        self.taskLayout.addWidget(self.header)
        self.taskLayout.addWidget(self.description)
        self.taskLayout.addWidget(self.artifactTemplates)
        self.taskLayout.addWidget(self.artifacts)
        self.taskLayout.addLayout(self.subtasksLayout)

        # set initial visibility of widgets
        self.expandCollapse()

        self.layout = QHBoxLayout()
        self.layout.addLayout(self.expandCollapseLayout)
        self.layout.addLayout(self.taskLayout)
        self.setLayout(self.layout)

    def expandCollapse(self):
        self.expanded = not self.expanded
        self.description.setVisible(self.expanded)
        self.artifactTemplates.setVisible(self.expanded)
        self.artifacts.setVisible(self.expanded)
        for subtask in self.subtasks:
            subtask.setVisible(self.expanded)
        icon: str = "fa5s.chevron-down" if self.expanded else "fa5s.chevron-right"
        self.expandCollapseButton.setIcon(qta.icon(icon))