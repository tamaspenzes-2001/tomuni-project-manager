from PySide6.QtWidgets import QWidget, QSpacerItem, QVBoxLayout
from UI.Sidebar.TemplatesSection import TemplatesSection
from UI.Sidebar.ProjectsSection import ProjectsSection

class Sidebar(QWidget):
    def __init__(self):
        super().__init__()
        self.templatesSection = TemplatesSection()
        self.projectsSection = ProjectsSection()

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.templatesSection)
        self.layout.addWidget(self.projectsSection)
        self.layout.addStretch()
        self.setLayout(self.layout)