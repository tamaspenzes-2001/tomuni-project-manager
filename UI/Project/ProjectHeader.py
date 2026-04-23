from PySide6.QtWidgets import QWidget, QLabel, QToolButton, QMenu, QHBoxLayout
from PySide6.QtGui import QAction
import qtawesome as qta
from typing import Dict

class ProjectHeader(QWidget):
    def __init__(self, projectData: Dict):
        super().__init__()
        self.projectData: Dict = projectData

        self.name = QLabel(projectData["name"])
        self.menuButton = QToolButton()
        self.menuButton.setAutoRaise(True)
        self.menuButton.setPopupMode(QToolButton.InstantPopup)
        self.menuButton.setStyleSheet(
            """
            QToolButton::menu-indicator {
                width: 0px;
                width: 0px;
            }
            """
        )
        self.menuButton.setIcon(qta.icon("msc.triangle-down"))
        self.menu = QMenu()
        self.menuButton.setMenu(self.menu)

        self.projectSettingsAction = QAction("Project settings")
        self.projectSettingsAction.triggered.connect(self.modifyProjectSettings)
        self.createAction = QAction("Create a template from this project")
        self.createAction.triggered.connect(self.createTemplate)
        self.completeAction = QAction("Mark project as completed")
        self.completeAction.triggered.connect(self.markAsCompleted)

        self.menu.addAction(self.projectSettingsAction)
        self.menu.addAction(self.createAction)
        self.menu.addAction(self.completeAction)

        self.date = QLabel("Started: " + projectData["date"])

        self.layout = QHBoxLayout()
        self.layout.addWidget(self.name)
        self.layout.addWidget(self.menuButton)
        self.layout.addStretch()
        self.layout.addWidget(self.date)
        self.setLayout(self.layout)

    def modifyProjectSettings(self):
        pass

    def createTemplate(self):
        pass

    def markAsCompleted(self):
        pass
