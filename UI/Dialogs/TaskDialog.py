from PySide6.QtWidgets import (QLabel, QLineEdit, QTextEdit, QPushButton, QToolButton, QTabWidget,
                                QVBoxLayout, QHBoxLayout, QDialog, QWidget)
from PySide6.QtCore import Qt
from PySide6.QtGui import QTextCursor, QTextDocument
import qtawesome as qta
from typing import Dict

class TaskDialog(QDialog):
    def __init__(self, data: Dict = {}):
        super().__init__()
        action: str = "Edit" if data else "Create"
        self.setWindowTitle(f"{action} task")

        self.nameLabel = QLabel(f"Name of task:")
        self.nameField = QLineEdit(data["name"] if data else "")

        self.nameLayout = QVBoxLayout()
        self.nameLayout.addWidget(self.nameLabel)
        self.nameLayout.addWidget(self.nameField)

        self.descriptionLabel = QLabel("Description:")
        
        self.boldButton = QToolButton()
        self.boldButton.setIcon(qta.icon("fa5s.bold"))
        self.boldButton.clicked.connect(self.formatBold)
        self.italicButton = QToolButton()
        self.italicButton.setIcon(qta.icon("ph.text-italic"))
        self.italicButton.clicked.connect(self.formatItalic)
        
        self.markdownEditorHeaderLayout = QHBoxLayout()
        self.markdownEditorHeaderLayout.addWidget(self.boldButton)
        self.markdownEditorHeaderLayout.addWidget(self.italicButton)
        self.markdownEditorHeaderLayout.addStretch()

        self.descriptionField = QTextEdit(data["description"] if data else "")
        self.descriptionField.textChanged.connect(self.updatePreview)

        self.renderedDescription = QLabel()
        self.updatePreview()

        self.description = QTabWidget()
        self.descriptionEditTab = QWidget()
        self.descriptionEditLayout = QVBoxLayout()
        self.descriptionEditLayout.addLayout(self.markdownEditorHeaderLayout)
        self.descriptionEditLayout.addWidget(self.descriptionField)
        self.descriptionEditTab.setLayout(self.descriptionEditLayout)
        self.description.addTab(self.descriptionEditTab, "Edit")
        self.descriptionPreviewTab = QWidget()
        self.descriptionPreviewLayout = QVBoxLayout()
        self.descriptionPreviewLayout.addWidget(self.renderedDescription)
        self.descriptionPreviewLayout.addStretch()
        self.descriptionPreviewTab.setLayout(self.descriptionPreviewLayout)
        self.description.addTab(self.descriptionPreviewTab, "Preview")
        
        self.descriptionLayout = QVBoxLayout()
        self.descriptionLayout.addWidget(self.descriptionLabel)
        self.descriptionLayout.addWidget(self.description)

        self.okButton = QPushButton("Ok")
        self.okButton.clicked.connect(self.okAction)
        self.cancelButton = QPushButton("Cancel")
        self.cancelButton.clicked.connect(self.cancelAction)

        self.dialogButtonLayout = QHBoxLayout()
        self.dialogButtonLayout.addStretch()
        self.dialogButtonLayout.addWidget(self.okButton)
        self.dialogButtonLayout.addWidget(self.cancelButton)

        self.layout = QVBoxLayout()
        self.layout.addLayout(self.nameLayout)
        self.layout.addLayout(self.descriptionLayout)
        self.layout.addLayout(self.dialogButtonLayout)
        self.setLayout(self.layout)

    def formatBold(self):
        cursor: QTextCursor = self.descriptionField.textCursor()
        if cursor.hasSelection():
            selected_text: str = cursor.selectedText()
            formatted_text: str = f"**{selected_text}**"
            cursor.insertText(formatted_text)
        else:
            cursor.insertText("****")
            pos: int = cursor.position()
            cursor.setPosition(pos - 2)
            self.descriptionField.setTextCursor(cursor)

    def formatItalic(self):
        cursor: QTextCursor = self.descriptionField.textCursor()
        if cursor.hasSelection():
            selected_text: str = cursor.selectedText()
            formatted_text: str = f"*{selected_text}*"
            cursor.insertText(formatted_text)
        else:
            cursor.insertText("**")
            pos: int = cursor.position()
            cursor.setPosition(pos - 1)
            self.descriptionField.setTextCursor(cursor)

    def updatePreview(self):
        markdown_text = self.descriptionField.toPlainText()
        doc = QTextDocument()
        doc.setMarkdown(markdown_text)
        self.renderedDescription.setText(doc.toHtml())

    def okAction(self):
        if self.validate():
            self.resultName: str = self.nameField.text()
            self.resultDescription: str = self.descriptionField.toPlainText()
            self.accept()

    def cancelAction(self):
        self.reject()

    def validate(self):
        valid: bool = True
        if not self.nameField.text():
            self.missingName = QLabel("Please provide a name!")
            self.nameLayout.addWidget(self.missingName)
            valid = False
        return valid
