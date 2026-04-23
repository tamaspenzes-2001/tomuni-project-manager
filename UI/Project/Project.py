from PySide6.QtWidgets import QWidget, QScrollArea, QHBoxLayout, QVBoxLayout
from typing import Dict
from UI.Project.ProjectHeader import ProjectHeader
from UI.Project.Phase import Phase

class Project(QWidget):
    def __init__(self, projectData: Dict):
        super().__init__()
        self.header = ProjectHeader(projectData)
        self.scrollArea = QScrollArea()
        self.openedProject = QWidget()
        self.openedProjectLayout = QHBoxLayout()
        self.openedProject.setLayout(self.openedProjectLayout)
        self.scrollArea.setWidget(self.openedProject)
        self.scrollArea.setWidgetResizable(True)
        for phase in projectData["phases"]:
            self.openedProjectLayout.addWidget(Phase(phase))
        
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.header)
        self.layout.addWidget(self.scrollArea)
        self.setLayout(self.layout)