from PySide6.QtWidgets import QWidget, QVBoxLayout, QSplitter
from PySide6.QtCore import Qt
from UI.Sidebar.TemplatesSection import TemplatesSection
from UI.Sidebar.ProjectsSection import ProjectsSection

class Sidebar(QSplitter):
    def __init__(self):
        super().__init__()
        self.templatesSection = TemplatesSection()
        self.projectsSection = ProjectsSection()

        self.addWidget(self.templatesSection)
        self.addWidget(self.projectsSection)

        self.setOrientation(Qt.Vertical)