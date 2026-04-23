from PySide6.QtWidgets import QWidget, QScrollArea, QHBoxLayout, QVBoxLayout
from UI.Project.ProjectHeader import ProjectHeader
from UI.Project.Phase import Phase

class Project(QWidget):
    def __init__(self, projectData):
        super().__init__()
        self.header = ProjectHeader(projectData["name"])
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