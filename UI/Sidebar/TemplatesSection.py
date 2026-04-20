from PySide6.QtWidgets import QWidget, QDialog, QLabel, QScrollArea, QPushButton, QVBoxLayout, QSizePolicy
from UI.Sidebar.TemplatesMenuEntry import TemplatesMenuEntry
from UI.Dialogs.ProjectDialog import ProjectDialog

class TemplatesSection(QWidget):
    def __init__(self):
        super().__init__()
        self.heading = QLabel("Templates")
        self.menuScrollArea = QScrollArea()
        self.menu = QWidget()
        self.menuLayout = QVBoxLayout()
        self.menuLayout.addStretch()
        self.menu.setLayout(self.menuLayout)
        self.menuScrollArea.setWidget(self.menu)
        self.menuScrollArea.setWidgetResizable(True)
        self.createButton = QPushButton("Create template")
        self.createButton.clicked.connect(self.createTemplate)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.heading)
        self.layout.addWidget(self.menuScrollArea)
        self.layout.addWidget(self.createButton)
        self.setLayout(self.layout)

    def createTemplate(self):
        dialog = ProjectDialog(template=True)
        # print(name, phases)
        result = dialog.exec()
        if result == QDialog.Accepted:
            newTemplate = TemplatesMenuEntry(dialog.resultName)
            # add new item above the stretch (QSpacerItem)
            self.menuLayout.insertWidget(self.menuLayout.count() - 1, newTemplate)
