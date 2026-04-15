from PySide6.QtCore import QSettings, QByteArray
from PySide6.QtWidgets import QApplication
from DataManager.ConfigManager import ConfigManager
from DataManager.DatabaseManager import DatabaseManager
from UI.AppUI import AppUI

class App(AppUI):
    def __init__(self, app: QApplication):
        super().__init__()
        self.app: QApplication = app
        self.confManager = ConfigManager()
        self.dbManager = DatabaseManager()
        self.settings = QSettings("Tamás Pénzes", "TomUni")
        self.readSettings()
        
    def writeSettings(self):
        self.settings.setValue("geometry", self.saveGeometry())
        self.settings.setValue("splitterSizes", self.splitter.saveState())

    def readSettings(self):
        self.restoreGeometry(self.settings.value("geometry", QByteArray()))
        self.splitter.restoreState(self.settings.value("splitterSizes", QByteArray()))

    def closeEvent(self, event):
        self.writeSettings()
        event.accept()