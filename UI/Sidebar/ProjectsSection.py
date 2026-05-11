from PySide6.QtWidgets import QWidget, QLabel, QTabWidget, QVBoxLayout
from UI.Sidebar.InProgressProjectsTab import InProgressProjectsTab
from UI.Sidebar.FinishedProjectsTab import FinishedProjectsTab
from DataManager.DatabaseManager import DatabaseManager

class ProjectsSection(QWidget):
    def __init__(self, dbManager: DatabaseManager):
        super().__init__()
        self.heading = QLabel("Projects")
        self.menu = QTabWidget()
        self.inProgressProjectsTab = InProgressProjectsTab(dbManager)
        self.finishedProjectsTab = FinishedProjectsTab(dbManager)
        self.menu.addTab(self.inProgressProjectsTab, "In progress")
        self.menu.addTab(self.finishedProjectsTab, "Finished")
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.heading)
        self.layout.addWidget(self.menu)
        self.setLayout(self.layout)