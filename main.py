import sys
from PySide6.QtWidgets import QApplication
from App import App


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName("TomUni")
    app.setDesktopFileName("io.github.tamaspenzes-2001.tomuni")

    window = App(app)
    window.show()
    sys.exit(app.exec())
