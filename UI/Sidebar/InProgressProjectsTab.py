from PySide6.QtWidgets import QWidget, QScrollArea, QPushButton, QDialog, QVBoxLayout
from UI.Dialogs.ProjectDialog import ProjectDialog
from UI.Sidebar.InProgressProjectsMenuEntry import InProgressProjectsMenuEntry

class InProgressProjectsTab(QWidget):
    def __init__(self):
        super().__init__()
        self.scrollArea = QScrollArea()
        self.menu = QWidget()
        self.menuLayout = QVBoxLayout()
        self.menuLayout.addStretch()
        self.menu.setLayout(self.menuLayout)
        self.scrollArea.setWidget(self.menu)
        self.scrollArea.setWidgetResizable(True)

        self.createButton = QPushButton("Create project")
        self.createButton.clicked.connect(self.createProject)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.scrollArea)
        self.layout.addWidget(self.createButton)
        self.setLayout(self.layout)

    def createProject(self):
        dialog = ProjectDialog()
        result = dialog.exec()
        if result == QDialog.DialogCode.Accepted:
            newProject = InProgressProjectsMenuEntry(dialog.resultName)
            self.menuLayout.insertWidget(self.menuLayout.count() - 1, newProject)