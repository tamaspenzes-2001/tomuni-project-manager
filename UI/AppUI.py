from PySide6.QtWidgets import QMainWindow, QSplitter, QWidget
from PySide6.QtCore import Qt
from datetime import date
from UI.Sidebar.Sidebar import Sidebar
from UI.Project.Project import Project

class AppUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.sidebar = Sidebar(self.dbManager)
        self.project = QWidget()

        self.splitter = QSplitter()
        
        self.splitter.addWidget(self.sidebar)
        self.splitter.addWidget(self.project)
        self.setCentralWidget(self.splitter)

    def loadProject(self, projectData):
        self.project.deleteLater()

        self.project = Project(projectData, self.dbManager, self.confManager)
        self.splitter.addWidget(self.project)
        self.splitter.setCollapsible(1, False)