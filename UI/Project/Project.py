from PySide6.QtWidgets import QWidget, QScrollArea, QHBoxLayout, QVBoxLayout
from typing import Dict
from UI.Project.ProjectHeader import ProjectHeader
from UI.Project.Phase import Phase
from DataManager.DatabaseManager import DatabaseManager

class Project(QWidget):
    def __init__(self, projectData: Dict, dbManager: DatabaseManager):
        super().__init__()
        self.header = ProjectHeader(projectData, dbManager)
        self.scrollArea = QScrollArea()
        self.phasesContainer = QWidget()
        self.phasesLayout = QHBoxLayout()
        self.phasesContainer.setLayout(self.phasesLayout)
        self.scrollArea.setWidget(self.phasesContainer)
        self.scrollArea.setWidgetResizable(True)
        self.phases: Dict = {}

        for phase_data in projectData["phases"]:
            phase_widget = Phase(phase_data, dbManager)
            self.phases[phase_data["id"]] = phase_widget
            self.phasesLayout.addWidget(phase_widget)
        
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.header)
        self.layout.addWidget(self.scrollArea)
        self.setLayout(self.layout)