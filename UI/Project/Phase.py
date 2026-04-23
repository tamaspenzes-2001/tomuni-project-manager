from PySide6.QtWidgets import QWidget, QLabel, QPushButton, QScrollArea, QVBoxLayout
from typing import Dict

class Phase(QWidget):
    def __init__(self, phaseData: Dict):
        super().__init__()
        self.name = QLabel(phaseData["name"])
        self.scrollArea = QScrollArea()
        self.tasks = QWidget()
        self.tasksLayout = QVBoxLayout()
        self.tasks.setLayout(self.tasksLayout)
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
        pass
