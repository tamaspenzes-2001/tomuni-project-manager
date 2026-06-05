from PySide6.QtWidgets import QWidget, QDialog, QLabel, QScrollArea, QPushButton, QVBoxLayout, QSizePolicy
from PySide6.QtCore import Qt
from UI.Sidebar.TemplatesMenuEntry import TemplatesMenuEntry
from UI.Dialogs.ProjectDialog import ProjectDialog

class TemplatesSection(QWidget):
    def __init__(self):
        super().__init__()
        self.heading = QLabel("Templates")
        self.heading.setProperty("class", "heading")
        self.heading.setAlignment(Qt.AlignCenter)
        self.menuScrollArea = QScrollArea()
        self.menu = QWidget()
        self.menu.setProperty("class", "content-box")
        self.menuLayout = QVBoxLayout()
        self.menuLayout.addStretch()
        self.menuLayout.setSpacing(0)
        self.menuLayout.setContentsMargins(0, 0, 0, 0)
        self.menu.setLayout(self.menuLayout)
        self.menuScrollArea.setWidget(self.menu)
        self.menuScrollArea.setWidgetResizable(True)
        self.createButton = QPushButton("Create template")
        self.createButton.setProperty("class", "button blue-button")
        self.createButton.clicked.connect(self.createTemplate)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.heading)
        self.layout.addWidget(self.menuScrollArea)
        self.layout.addWidget(self.createButton)
        self.layout.setSpacing(0)
        self.setLayout(self.layout)

    def createTemplate(self):
        dialog = ProjectDialog(template=True)
        result: int = dialog.exec()
        if result == QDialog.Accepted:
            newTemplate = TemplatesMenuEntry(dialog.resultName)
            # add new item above the stretch (QSpacerItem)
            self.menuLayout.insertWidget(self.menuLayout.count() - 1, newTemplate)
