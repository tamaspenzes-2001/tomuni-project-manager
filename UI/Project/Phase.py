from PySide6.QtWidgets import QWidget, QLabel, QPushButton, QScrollArea, QDialog, QVBoxLayout
from PySide6.QtCore import Qt
from PySide6.QtGui import QTextDocument
from typing import Dict
from UI.Project.Task import Task
from UI.Dialogs.TaskDialog import TaskDialog

class Phase(QWidget):
    def __init__(self, phaseData: Dict):
        super().__init__()
        self.name = QLabel(phaseData["name"])
        self.scrollArea = QScrollArea()
        self.tasks = QWidget()
        self.tasksLayout = QVBoxLayout()
        self.tasks.setLayout(self.tasksLayout)
        for task in phaseData["tasks"]:
            self.tasksLayout.addWidget(Task(task))
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
        result = dialog.exec()
        if result == QDialog.DialogCode.Accepted:
            doc = QTextDocument()
            doc.setMarkdown(dialog.resultDescription)
            newTask = Task({
                    "name": dialog.resultName,
                    "description": doc.toHtml(),
                    "artifactTemplates": [],
                    "artifacts": [],
                    "state": Qt.Unchecked,
                    "subtasks": []
                })
            self.tasksLayout.insertWidget(self.tasksLayout.count() - 1, newTask)