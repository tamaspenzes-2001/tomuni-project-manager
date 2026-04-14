from PySide6.QtWidgets import QMainWindow

class App(QMainWindow):
    def __init__(self, app):
        self.app = app
        super().__init__()