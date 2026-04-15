from PySide6.QtWidgets import QMainWindow, QHBoxLayout, QSplitter
from UI.Sidebar.Sidebar import Sidebar
from UI.Project.Project import Project

class AppUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.sidebar = Sidebar()
        self.project = Project()
        self.splitter = QSplitter()
        self.splitter.addWidget(self.sidebar)
        self.splitter.addWidget(self.project)
        self.setCentralWidget(self.splitter)