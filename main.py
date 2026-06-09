import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon
from App import App
from helpers import assetPath


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName("TomUni")
    app.setDesktopFileName("io.github.tamaspenzes2001.tomuni")
    app.setWindowIcon(QIcon(assetPath("logo.png")))

    with open(assetPath("style.css"), "r") as stylesheet:
        app.setStyleSheet(stylesheet.read())

    window = App(app)
    window.show()
    sys.exit(app.exec())
