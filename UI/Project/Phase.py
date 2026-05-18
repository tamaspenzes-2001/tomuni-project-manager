from PySide6.QtWidgets import QWidget, QLabel, QPushButton, QScrollArea, QDialog, QVBoxLayout
from PySide6.QtCore import Qt
from PySide6.QtGui import QTextDocument
from typing import Dict
from UI.Project.Task import Task
from UI.Dialogs.TaskDialog import TaskDialog
from DataManager.DatabaseManager import DatabaseManager

class Phase(QWidget):
    def __init__(self, phaseData: Dict, dbManager: DatabaseManager):
        super().__init__()
        self.phaseData: Dict = phaseData
        self.dbManager: DatabaseManager = dbManager
        
        self.name = QLabel(phaseData["name"])
        self.scrollArea = QScrollArea()
        self.tasks = QWidget()
        self.tasksLayout = QVBoxLayout()
        self.tasks.setLayout(self.tasksLayout)
        for task in phaseData["tasks"]:
            self.tasksLayout.addWidget(Task(task, dbManager))
        self.tasksLayout.addStretch()

        self.scrollArea.setWidget(self.tasks)
        self.scrollArea.setWidgetResizable(True)
        self.addTaskButton = QPushButton("Add task")
        self.addTaskButton.clicked.connect(self.addTask)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.name)
        self.layout.addWidget(self.scrollArea)
        self.layout.addWidget(self.addTaskButton)
        self.layout.addStretch()
        self.setLayout(self.layout)

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

                newTask = Task(newTaskData, self.dbManager)
                self.tasksLayout.insertWidget(self.tasksLayout.count() - 1, newTask)

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