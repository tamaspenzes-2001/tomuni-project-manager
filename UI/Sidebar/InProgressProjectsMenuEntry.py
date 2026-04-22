from PySide6.QtWidgets import QWidget, QLabel, QPushButton, QHBoxLayout
import qtawesome as qta
from UI.Sidebar.FinishedProjectsMenuEntry import FinishedProjectsMenuEntry

class InProgressProjectsMenuEntry(QWidget):
    def __init__(self, name):
        super().__init__()
        self.name = QLabel(name)
        self.completeButton = QPushButton()
        self.completeButton.setIcon(qta.icon("fa5s.check"))

        self.layout = QHBoxLayout()
        self.layout.addWidget(self.name)
        self.layout.addWidget(self.completeButton)
        self.setLayout(self.layout)

        self.mouseReleaseEvent = self.openProject
        self.completeButton.clicked.connect(self.completeProject)

    def openProject(self):
        pass

    def completeProject(self):
        projectsSection = self.parent().parent().parent().parent().parent().parent().parent()
        finishedProjectsMenuLayout = projectsSection.finishedProjectsTab.menuLayout
        finishedProject = FinishedProjectsMenuEntry(self.name.text())
        finishedProjectsMenuLayout.insertWidget(finishedProjectsMenuLayout.count() - 1, finishedProject)
        self.deleteLater()
