import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon
from App import App
from helpers import assetPath


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName("TomUni")
    app.setDesktopFileName("io.github.tamaspenzes-2001.tomuni")
    app.setWindowIcon(QIcon(assetPath("logo.png")))

    window = App(app)
    window.show()
    sys.exit(app.exec())
