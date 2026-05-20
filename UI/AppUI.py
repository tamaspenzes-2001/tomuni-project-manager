from PySide6.QtWidgets import QMainWindow, QSplitter, QWidget, QDialog
from PySide6.QtCore import Qt
from datetime import date
from UI.Sidebar.Sidebar import Sidebar
from UI.Project.Project import Project
from UI.Dialogs.SettingsDialog import SettingsDialog

class AppUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.sidebar = Sidebar(self.dbManager)
        self.project = QWidget()

        self.splitter = QSplitter()
        
        self.splitter.addWidget(self.sidebar)
        self.splitter.addWidget(self.project)
        self.setCentralWidget(self.splitter)

        self.menuBar = self.menuBar()

        self.fileMenu = self.menuBar.addMenu("File")
        self.createTemplateAction = self.fileMenu.addAction("Create template")
        self.createTemplateAction.triggered.connect(self.sidebar.templatesSection.createTemplate)
        self.createProjectAction = self.fileMenu.addAction("Create project")
        self.createProjectAction.triggered.connect(self.sidebar.projectsSection.inProgressProjectsTab.createProject)
        self.settingsAction = self.fileMenu.addAction("Settings")
        self.settingsAction.triggered.connect(self.modifySettings)
        self.quitAction = self.fileMenu.addAction("Quit")
        self.quitAction.triggered.connect(self.app.quit)

        self.aboutMenu = self.menuBar.addMenu("About")
        self.aboutAction = self.aboutMenu.addAction("About TomUni")
        self.aboutAction.triggered.connect(self.showAbout)

    def loadProject(self, projectData):
        self.project.deleteLater()

        self.project = Project(projectData, self.dbManager, self.confManager)
        self.splitter.addWidget(self.project)
        self.splitter.setCollapsible(1, False)

    def modifySettings(self):
        dialog = SettingsDialog(self.confManager.config)
        result = dialog.exec()
        if result == QDialog.DialogCode.Accepted:
            self.confManager.config = {
                "delConfirmProjectTemplates": dialog.resultDelConfirmProjectTemplates,
                "delConfirmTasks": dialog.resultDelConfirmTasks,
                "dateFormat": dialog.resultDateFormat,
                "encryptionEnabled": dialog.resultEncryption,
                "encryptionPassword": dialog.resultEncryptionPassword
            }
            self.confManager.saveConfig()

    def showAbout(self):
        pass