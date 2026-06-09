from PySide6.QtWidgets import QWidget, QScrollArea, QPushButton, QDialog, QVBoxLayout
from PySide6.QtCore import QDate
from UI.Dialogs.ProjectDialog import ProjectDialog
from UI.Sidebar.InProgressProjectsMenuEntry import InProgressProjectsMenuEntry
from DataManager.DatabaseManager import DatabaseManager

class InProgressProjectsTab(QWidget):
    def __init__(self, dbManager: DatabaseManager):
        super().__init__()
        self.dbManager: dbManager = dbManager

        self.scrollArea = QScrollArea()
        self.menu = QWidget()
        self.menuLayout = QVBoxLayout()
        projects, _ = dbManager.executeQuery(
            """
            SELECT id, name FROM Project
            WHERE state = 'InProgress' AND template = 0
            ORDER BY startDate DESC
            """
        )
        while projects.next():
            menuEntry = InProgressProjectsMenuEntry(
                projects.value("name"), projects.value("id"), dbManager
            )
            self.menuLayout.addWidget(menuEntry)
        self.menuLayout.addStretch()
        self.menuLayout.setContentsMargins(0, 0, 0, 0)
        self.menuLayout.setSpacing(0)
        self.menu.setLayout(self.menuLayout)
        self.scrollArea.setWidget(self.menu)
        self.scrollArea.setWidgetResizable(True)

        self.createButton = QPushButton("Create project")
        self.createButton.setProperty("class", "square-button blue-button")
        self.createButton.clicked.connect(self.createProject)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.scrollArea)
        self.layout.addWidget(self.createButton)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.setLayout(self.layout)

    def createProject(self):
        dialog = ProjectDialog()
        result: int = dialog.exec()
        if result == QDialog.DialogCode.Accepted:
            maxIdQuery, _ = self.dbManager.executeQuery("SELECT MAX(id) AS max_id FROM Project")
            maxIdQuery.next()
            maxId: str = maxIdQuery.value("max_id")
            newId: int = (int(maxId) + 1) if maxId else 1

            newProject = InProgressProjectsMenuEntry(dialog.resultName, newId, self.dbManager)
            self.menuLayout.insertWidget(0, newProject)

            dbOperations: list = []
            
            dbOperations.append([
                "INSERT INTO Project (name, startDate) VALUES (?, ?)",
                [dialog.resultName, QDate.currentDate().toString("yyyy-MM-dd")]
            ])
            for phase in dialog.resultPhases:
                dbOperations.append([
                    "INSERT INTO Phase (name, projectId) VALUES (?, ?)",
                    [phase["name"], newId]
                ])
            self.dbManager.executeTransaction(dbOperations)