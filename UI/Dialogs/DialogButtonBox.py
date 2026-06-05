from PySide6.QtWidgets import QWidget, QHBoxLayout, QPushButton

class DialogButtonBox(QWidget):
    def __init__(self):
        super().__init__()
        self.okButton = QPushButton("Ok")
        self.okButton.setProperty("class", "blue-button")
        self.cancelButton = QPushButton("Cancel")
        self.cancelButton.setProperty("class", "dark-red-button")

        self.layout = QHBoxLayout()
        self.layout.addStretch()
        self.layout.addWidget(self.okButton)
        self.layout.addWidget(self.cancelButton)
        self.setLayout(self.layout)