from PySide6.QtWidgets import QScrollArea, QWidget, QVBoxLayout
from UI.Sidebar.FinishedProjectsMenuEntry import FinishedProjectsMenuEntry
from DataManager.DatabaseManager import DatabaseManager

class FinishedProjectsTab(QScrollArea):
    def __init__(self, dbManager: DatabaseManager):
        super().__init__()
        self.menu = QWidget()
        self.menuLayout = QVBoxLayout()
        projects, _ = dbManager.executeQuery(
            """
            SELECT id, name FROM Project
            WHERE state = 'Finished' AND template = 0
            ORDER BY finishDate DESC
            """
        )
        while projects.next():
            menuEntry = FinishedProjectsMenuEntry(
                projects.value("name"), projects.value("id"), dbManager
            )
            self.menuLayout.addWidget(menuEntry)
        self.menuLayout.addStretch()
        self.menu.setLayout(self.menuLayout)
        self.setWidget(self.menu)
        self.setWidgetResizable(True)