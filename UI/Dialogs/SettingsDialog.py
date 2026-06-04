from PySide6.QtWidgets import QDialog, QLabel, QCheckBox, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout
from PySide6.QtCore import Qt
from typing import Dict

class SettingsDialog(QDialog):
    def __init__(self, config: Dict):
        super().__init__()
        self.setWindowTitle("Settings")

        self.delConfirmLabel = QLabel("Deletion confirmation for...")
        self.delConfirmLabel.setProperty("class", "dialog-heading")
        self.delConfirmProjectTemplates = QCheckBox("Project templates")
        self.delConfirmProjectTemplates.setChecked(config["delConfirmProjectTemplates"])
        self.delConfirmTasks = QCheckBox("Tasks")
        self.delConfirmTasks.setChecked(config["delConfirmTasks"])

        self.otherSettingsLabel = QLabel("Other settings")
        self.otherSettingsLabel.setProperty("class", "dialog-heading")

        self.dateFormatLabel = QLabel("Date format (<a href='https://www.strfti.me/'>strftime</a>):")
        self.dateFormatLabel.setOpenExternalLinks(True)
        self.dateFormatField = QLineEdit()
        self.dateFormatField.setText(config["dateFormat"])

        self.dateFormatLayout = QVBoxLayout()
        self.dateFormatLayout.addWidget(self.dateFormatLabel)
        self.dateFormatLayout.addWidget(self.dateFormatField)

        self.encryption = QCheckBox("Enable password encryption")
        self.encryption.setChecked(config["encryptionEnabled"])

        self.encryption.checkStateChanged.connect(self.toggleEncryption)
        self.encryptionPasswordLabel = QLabel("Encryption password:")
        self.encryptionPasswordLabel.setVisible(config["encryptionEnabled"])
        self.encryptionPasswordField = QLineEdit()
        self.encryptionPasswordField.setText(config["encryptionPassword"])
        self.encryptionPasswordField.setVisible(config["encryptionEnabled"])

        self.encryptionLayout = QVBoxLayout()
        self.encryptionLayout.addWidget(self.encryption)
        self.encryptionLayout.addWidget(self.encryptionPasswordLabel)
        self.encryptionLayout.addWidget(self.encryptionPasswordField)

        self.okButton = QPushButton("Ok")
        self.okButton.clicked.connect(self.okAction)
        self.okButton.setProperty("class", "blue-button")
        self.cancelButton = QPushButton("Cancel")
        self.cancelButton.clicked.connect(self.cancelAction)
        self.cancelButton.setProperty("class", "dark-red-button")

        self.dialogButtonLayout = QHBoxLayout()
        self.dialogButtonLayout.addStretch()
        self.dialogButtonLayout.addWidget(self.okButton)
        self.dialogButtonLayout.addWidget(self.cancelButton)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.delConfirmLabel)
        self.layout.addWidget(self.delConfirmProjectTemplates)
        self.layout.addWidget(self.delConfirmTasks)
        self.layout.addWidget(self.otherSettingsLabel)
        self.layout.addLayout(self.dateFormatLayout)
        self.layout.addLayout(self.encryptionLayout)
        self.layout.addStretch()
        self.layout.addLayout(self.dialogButtonLayout)

        self.setLayout(self.layout)

    def toggleEncryption(self, state):
        enabled = state == Qt.Checked
        self.encryptionPasswordLabel.setVisible(enabled)
        self.encryptionPasswordField.setVisible(enabled)

    def okAction(self):
        if self.validate():
            self.resultDelConfirmProjectTemplates: bool = self.delConfirmProjectTemplates.isChecked()
            self.resultDelConfirmTasks: bool = self.delConfirmTasks.isChecked()
            self.resultDateFormat: str = self.dateFormatField.text()
            self.resultEncryption: bool = self.encryption.isChecked()
            self.resultEncryptionPassword: str = self.encryptionPasswordField.text()
            self.accept()

    def cancelAction(self):
        self.reject()

    def validate(self):
        valid: bool = True
        if not self.dateFormatField.text():
            self.missingDateFormat = QLabel("Please provide a date format!")
            self.dateFormatLayout.addWidget(self.missingDateFormat)
            valid = False
        if self.encryption.isChecked() and not self.encryptionPasswordField.text():
            self.missingEncryptionPassword = QLabel("Please add an encryption password!")
            self.encryptionLayout.addWidget(self.missingEncryptionPassword)
            valid = False
        return valid