from PySide6.QtWidgets import (QDialog, QLabel, QLineEdit, QListWidget, QListWidgetItem, QPushButton,
                              QVBoxLayout, QHBoxLayout)
from PySide6.QtCore import Qt
from typing import Dict

class ProjectDialog(QDialog):
    def __init__(self, template: bool = False, data: Dict = {}):
        super().__init__()
        action: str = "Edit" if data else "Create"
        itemType: str = "project template" if template else "project"

        self.setWindowTitle(f"{action} {itemType}")

        self.nameLabel = QLabel(f"Name of {itemType}:")
        self.nameField = QLineEdit()
        if data:
            self.nameField.setText(data["name"])

        self.nameLayout = QVBoxLayout()
        self.nameLayout.addWidget(self.nameLabel)
        self.nameLayout.addWidget(self.nameField)

        self.phasesLabel = QLabel("Phases:")
        self.phasesField = QListWidget()
        phases = data["phases"] if data else ["Planning", "Implementation"]
        for phase in phases:
            newPhase = QListWidgetItem(phase, self.phasesField)
            newPhase.setFlags(newPhase.flags() | Qt.ItemIsEditable)

        self.phaseAddButton = QPushButton("Add")
        self.phaseAddButton.clicked.connect(self.addPhase)
        self.phaseEditButton = QPushButton("Edit")
        self.phaseEditButton.clicked.connect(self.editPhase)
        self.phaseDeleteButton = QPushButton("Delete")
        self.phaseDeleteButton.clicked.connect(self.deletePhase)
        self.phaseMoveUpButton = QPushButton("Move up")
        self.phaseMoveUpButton.clicked.connect(self.moveUpPhase)
        self.phaseMoveDownButton = QPushButton("Move down")
        self.phaseMoveDownButton.clicked.connect(self.moveDownPhase)

        self.phasesButtonLayout = QVBoxLayout()
        self.phasesButtonLayout.addWidget(self.phaseAddButton)
        self.phasesButtonLayout.addWidget(self.phaseEditButton)
        self.phasesButtonLayout.addWidget(self.phaseDeleteButton)
        self.phasesButtonLayout.addWidget(self.phaseMoveUpButton)
        self.phasesButtonLayout.addWidget(self.phaseMoveDownButton)
        self.phasesButtonLayout.addStretch()

        self.phasesEditorLayout = QHBoxLayout()
        self.phasesEditorLayout.addWidget(self.phasesField)
        self.phasesEditorLayout.addLayout(self.phasesButtonLayout)

        self.phasesLayout = QVBoxLayout()
        self.phasesLayout.addWidget(self.phasesLabel)
        self.phasesLayout.addLayout(self.phasesEditorLayout)

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
        self.layout.addLayout(self.phasesLayout)
        self.layout.addLayout(self.dialogButtonLayout)

        self.setLayout(self.layout)

    def addPhase(self):
        self.newPhase = QListWidgetItem(self.phasesField)
        self.newPhase.setFlags(self.newPhase.flags() | Qt.ItemIsEditable)
        self.phasesField.editItem(self.newPhase)

    def editPhase(self):
        selectedItem: QListWidgetItem = self.phasesField.currentItem()
        if selectedItem:
            self.phasesField.editItem(selectedItem)

    def deletePhase(self):
        itemIndex: int = self.phasesField.currentRow()
        if itemIndex >= 0:
            self.phasesField.takeItem(itemIndex)

    def moveUpPhase(self):
        itemIndex: int = self.phasesField.currentRow()
        if itemIndex >= 0:
            itemToMove: QListWidgetItem = self.phasesField.takeItem(itemIndex)
            self.phasesField.insertItem(itemIndex-1, itemToMove)
            self.phasesField.setCurrentItem(itemToMove)

    def moveDownPhase(self):
        itemIndex: int = self.phasesField.currentRow()
        if itemIndex >= 0:
            itemToMove: QListWidgetItem = self.phasesField.takeItem(itemIndex)
            self.phasesField.insertItem(itemIndex+1, itemToMove)
            self.phasesField.setCurrentItem(itemToMove)

    def okAction(self):
        if self.validate():
            self.resultName: str = self.nameField.text()
            self.resultPhases: List[str] = [self.phasesField.item(i).text() for i in range(self.phasesField.count())]
            self.accept()

    def cancelAction(self):
        self.reject()

    def validate(self):
        valid: bool = True
        if not self.nameField.text():
            self.missingName = QLabel("Please provide a name!")
            self.nameLayout.addWidget(self.missingName)
            valid = False
        if not self.phasesField.count():
            self.noPhase = QLabel("Please add at least one phase!")
            self.phasesLayout.addWidget(self.noPhase)
            valid = False
        return valid