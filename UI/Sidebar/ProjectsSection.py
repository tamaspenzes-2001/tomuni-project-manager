from PySide6.QtWidgets import QWidget, QLabel, QTabWidget, QVBoxLayout
from UI.Sidebar.InProgressProjectsTab import InProgressProjectsTab
from UI.Sidebar.FinishedProjectsTab import FinishedProjectsTab

class ProjectsSection(QWidget):
    def __init__(self):
        super().__init__()
        self.heading = QLabel("Projects")
        self.menu = QTabWidget()
        self.inProgressProjectsTab = InProgressProjectsTab()
        self.finishedProjectsTab = FinishedProjectsTab()
        self.menu.addTab(self.inProgressProjectsTab, "In progress")
        self.menu.addTab(self.finishedProjectsTab, "Finished")
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.heading)
        self.layout.addWidget(self.menu)
        self.setLayout(self.layout)