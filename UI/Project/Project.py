from PySide6.QtWidgets import QWidget, QScrollArea, QGridLayout, QVBoxLayout, QSizePolicy
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QResizeEvent
from typing import Dict
from UI.Project.ProjectHeader import ProjectHeader
from UI.Project.Phase import Phase
from DataManager.DatabaseManager import DatabaseManager
from DataManager.ConfigManager import ConfigManager

class Project(QWidget):
    def __init__(self, projectData: Dict, dbManager: DatabaseManager, confManager: ConfigManager):
        super().__init__()
        self.header = ProjectHeader(projectData, dbManager, confManager)

        self.scrollArea = QScrollArea()
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scrollArea.setProperty("class", "content-box")
        self.scrollArea.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.scrollArea.setWidgetResizable(True)

        self.phasesContainer = QWidget()
        self.phasesContainer.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        self.phasesContainer.setMinimumWidth(0)
        self.phasesLayout = QGridLayout()
        self.phasesContainer.setLayout(self.phasesLayout)
        self.scrollArea.setWidget(self.phasesContainer)

        self.phases: Dict = {}

        for i, phaseData in enumerate(projectData["phases"]):
            phaseWidget = Phase(phaseData, dbManager, confManager)
            self.phases[phaseData["id"]] = phaseWidget
            self.phasesLayout.addWidget(phaseWidget, 0, i, 1, 1)
            self.phasesLayout.setColumnStretch(i, 1)
        self.phasesLayout.setRowStretch(0, 1)

        self.phasesContainer.adjustSize()
        self.scrollArea.updateGeometry()
        
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.header)
        self.layout.addWidget(self.scrollArea)
        self.setLayout(self.layout)
        self.setMinimumWidth(400)

        QTimer.singleShot(0, self._fixInitialLayout)

    def _fixInitialLayout(self):
        for phase in self.phases.values():
            phase.updateGeometry()
            phase.update()
        self.updateGeometry()
        self.update()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        for phase in self.phases.values():
            phase.updateGeometry()
            phase.update()
        
        self.scrollArea.updateGeometry()
        self.update()
        self.phasesLayout.activate()