from PySide6.QtWidgets import QWidget, QLabel, QPushButton, QScrollArea, QSizePolicy, QDialog, QVBoxLayout
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QTextDocument
from typing import Dict
from UI.Project.Task import Task
from UI.Dialogs.TaskDialog import TaskDialog
from DataManager.DatabaseManager import DatabaseManager
from DataManager.ConfigManager import ConfigManager

class Phase(QWidget):
    def __init__(self, phaseData: Dict, dbManager: DatabaseManager, confManager: ConfigManager):
        super().__init__()
        self.phaseData: Dict = phaseData
        self.dbManager: DatabaseManager = dbManager
        self.confManager: ConfigManager = confManager
        
        self.name = QLabel(phaseData["name"])
        self.name.setProperty("class", "subheading bottom-border")

        self.scrollArea = QScrollArea()
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scrollArea.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        self.scrollArea.setFrameShape(QScrollArea.NoFrame)
        self.scrollArea.setProperty("class", "content-box")

        self.tasks = QWidget()
        self.tasks.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.tasks.setMinimumWidth(0)

        self.tasksLayout = QVBoxLayout()
        self.tasksLayout.setContentsMargins(0, 0, 0, 0)
        self.tasksLayout.setSpacing(0)
        self.tasks.setLayout(self.tasksLayout)

        for task in phaseData["tasks"]:
            taskWidget = Task(task, dbManager, confManager)
            self.tasksLayout.addWidget(taskWidget)
        self.tasksLayout.addStretch()

        self.scrollArea.setWidget(self.tasks)

        self.addTaskButton = QPushButton("Add task")
        self.addTaskButton.setProperty("class", "square-button blue-button")
        self.addTaskButton.clicked.connect(self.addTask)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.name)
        self.layout.addWidget(self.scrollArea)
        self.layout.addWidget(self.addTaskButton)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        self.setLayout(self.layout)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        self.setMinimumWidth(0)

    def sizeHint(self):
        maxWidth: int = 0
        for i in range(self.tasksLayout.count()):
            widget: Task = self.tasksLayout.itemAt(i).widget()
            if widget:
                width: int = widget.sizeHint().width()
                if width > maxWidth:
                    maxWidth = width
        
        baseHint: QSize = super().sizeHint()
        baseHint.setWidth(max(baseHint.width(), maxWidth + 20))
        return baseHint

    def minimumSizeHint(self):
        maxWidth: int = 0
        for i in range(self.tasksLayout.count()):
            widget: Task = self.tasksLayout.itemAt(i).widget()
            if widget:
                width: int = widget.minimumSizeHint().width()
                if width > maxWidth:
                    maxWidth = width
        
        baseHint: QSize = super().minimumSizeHint()
        baseHint.setWidth(max(baseHint.width(), maxWidth + 20))
        return baseHint

    def updateGeometry(self):
        self.tasks.updateGeometry()
        self.scrollArea.updateGeometry()
        
        for i in range(self.tasksLayout.count()):
            widget: Task = self.tasksLayout.itemAt(i).widget()
            if widget:
                widget.updateGeometry()
                widget.update()
        
        if self.parent():
            self.parent().updateGeometry()
            self.parent().update()
        
        super().updateGeometry()
        self.update()

    def addTask(self):
        dialog = TaskDialog()
        result: int = dialog.exec()
        if result == QDialog.DialogCode.Accepted:
            name: str = dialog.resultName
            description: str = dialog.resultDescription
            doc = QTextDocument()
            doc.setMarkdown(description)

            _, success = self.dbManager.executeQuery(
                """
                INSERT INTO Task (name, description, phaseId)
                VALUES (?, ?, ?)
                """,
                [name, description, self.phaseData["id"]]
            )
            if success:
                query, _ = self.dbManager.executeQuery("SELECT MAX(id) AS max_id FROM Task")
                query.next()
                maxId: int = query.value("max_id")
                
                newTaskData: Dict = {
                    "id": maxId,
                    "name": name,
                    "description": doc.toHtml(),
                    "artifactTemplates": [],
                    "artifacts": [],
                    "state": Qt.Unchecked,
                    "subtasks": []
                }

                self.phaseData["tasks"].append(newTaskData)

                newTask = Task(newTaskData, self.dbManager, self.confManager)
                self.tasksLayout.insertWidget(self.tasksLayout.count() - 1, newTask)

                self.updateGeometry()
                self.update()

                query, _ = self.dbManager.executeQuery(
                    "SELECT MAX(position) FROM Task WHERE phaseId = ? AND parentTaskId IS NULL",
                    [self.phaseData["id"]]
                )
                query.next()
                maxPos: int = query.value(0)
                newPosition: int = (maxPos + 1) if maxPos is not None else 0
                
                # Update the task with the correct position
                self.dbManager.executeQuery(
                    "UPDATE Task SET position = ? WHERE id = ?",
                    [newPosition, maxId]
                )