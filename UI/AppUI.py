from PySide6.QtWidgets import QMainWindow, QSplitter
from UI.Sidebar.Sidebar import Sidebar
from UI.Project.Project import Project

class AppUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.sidebar = Sidebar()
        self.project = Project({
            "name": "Todo app",
            "date": "2026-04-23",
            "phases": ["Implementation", "Testing"]
        })

        self.splitter = QSplitter()
        self.splitter.addWidget(self.sidebar)
        self.splitter.addWidget(self.project)
        self.splitter.setCollapsible(1, False)
        self.setCentralWidget(self.splitter)