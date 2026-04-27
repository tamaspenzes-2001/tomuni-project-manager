from PySide6.QtWidgets import QWidget, QCheckBox, QLabel, QToolButton, QMenu, QHBoxLayout, QMessageBox
from PySide6.QtGui import QAction
import qtawesome as qta
from typing import Dict

class TaskHeader(QWidget):
    def __init__(self, taskData: Dict):
        super().__init__()
        self.taskData = taskData

        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        self.state = QCheckBox(taskData["name"])
        self.state.setTristate()
        self.state.setCheckState(taskData["state"])
        self.layout.addWidget(self.state)
        self.layout.addStretch()

        if "startDate" in taskData:
            if "completionDate" in taskData:
                self.date = QLabel(f"{taskData['startDate']} - {taskData['completionDate']}")
            else:
                self.date = QLabel(f"Started at: {taskData['startDate']}")
            self.layout.addWidget(self.date)

        self.menuButton = QToolButton()
        self.menuButton.setAutoRaise(True)
        self.menuButton.setPopupMode(QToolButton.InstantPopup)
        self.menuButton.setStyleSheet(
            """
            QToolButton::menu-indicator {
                width: 0px;
                width: 0px;
            }
            """
        )
        self.menuButton.setIcon(qta.icon("msc.triangle-down"))
        self.layout.addWidget(self.menuButton)

        self.menu = QMenu()
        self.editAction = QAction("Edit")
        self.editAction.triggered.connect(self.edit)
        self.deleteAction = QAction("Delete")
        self.deleteAction.triggered.connect(self.delete)
        self.moveUpAction = QAction("Move up")
        self.moveUpAction.triggered.connect(self.moveUp)
        self.moveDownAction = QAction("Move down")
        self.moveDownAction.triggered.connect(self.moveDown)
        self.addSubtaskAction = QAction("Add subtask")
        self.addSubtaskAction.triggered.connect(self.addSubtask)
        self.menu.addActions([
            self.editAction, self.deleteAction, self.moveUpAction,
            self.moveDownAction, self.addSubtaskAction
        ])
        self.menuButton.setMenu(self.menu)
        
    def edit(self):
        pass

    def delete(self):
        confirmation = QMessageBox.question(self, "Delete task",
                                    f"Delete task {self.taskData['name']}? It will be permanently lost!",
                                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if confirmation == QMessageBox.Yes:
            self.parent().deleteLater()

    def moveUp(self):
        taskWidget = self.parent()
        layout = None
        # get layout based on whether the task is a subtask
        if hasattr(taskWidget.parent(), "subtasksLayout"):
            layout = taskWidget.parent().subtasksLayout
        else:
            layout = taskWidget.parent().parent().parent().parent().tasksLayout
        currentIndex = -1
        for i in range(layout.count()):
            if layout.itemAt(i).widget() == taskWidget:
                currentIndex = i
                break
        if currentIndex > 0:
            layout.removeWidget(taskWidget)
            layout.insertWidget(currentIndex - 1, taskWidget)

    def moveDown(self):
        taskWidget = self.parent()
        layout = None
        # get layout based on whether the task is a subtask
        if hasattr(taskWidget.parent(), "subtasksLayout"):
            layout = taskWidget.parent().subtasksLayout
        else:
            layout = taskWidget.parent().parent().parent().parent().tasksLayout
        currentIndex = -1
        for i in range(layout.count()):
            if layout.itemAt(i).widget() == taskWidget:
                currentIndex = i
                break
        if currentIndex < layout.count()-1:
            layout.removeWidget(taskWidget)
            layout.insertWidget(currentIndex + 1, taskWidget)

    def addSubtask(self):
        pass