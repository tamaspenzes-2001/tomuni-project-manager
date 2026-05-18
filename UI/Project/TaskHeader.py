from PySide6.QtWidgets import (QWidget, QCheckBox, QLabel, QToolButton, QMenu,
                                QHBoxLayout, QVBoxLayout, QMessageBox, QDialog)
from PySide6.QtGui import QAction, QTextDocument
from PySide6.QtCore import Qt, QDate
import qtawesome as qta
from typing import Dict
from UI.Dialogs.TaskDialog import TaskDialog
from DataManager.DatabaseManager import DatabaseManager

class TaskHeader(QWidget):
    def __init__(self, taskData: Dict, dbManager: DatabaseManager):
        super().__init__()
        self.taskData: Dict = taskData
        self.dbManager: DatabaseManager = dbManager

        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        self.task = QCheckBox(taskData["name"])
        self.task.setTristate()
        self.task.setCheckState(taskData["state"])

        _originalMousePress = self.task.mousePressEvent

        def _customMousePress(event):
            if self.task.checkState() == Qt.Checked:
                return
            _originalMousePress(event)

        self.task.mousePressEvent = _customMousePress

        self.task.checkStateChanged.connect(self.changeState)
        self.layout.addWidget(self.task)
        self.layout.addStretch()

        self.date = QLabel("")
        self.layout.addWidget(self.date)

        # Initialize date label based on initial state
        self._updateDateLabel()

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

    def _updateDateLabel(self):
        state = self.task.checkState()
        hasStartDate = "startDate" in self.taskData and self.taskData["startDate"]
        hasCompletionDate = "completionDate" in self.taskData and self.taskData["completionDate"]
        
        if state == Qt.Unchecked:
            self.date.setVisible(False)
        elif state == Qt.PartiallyChecked:
            if hasStartDate:
                self.date.setText(f"Started at: {self.taskData['startDate']}")
                self.date.setVisible(True)
            else:
                self.date.setVisible(False)
        elif state == Qt.Checked:
            if hasStartDate:
                if hasCompletionDate:
                    self.date.setText(f"{self.taskData['startDate']} - {self.taskData['completionDate']}")
                else:
                    self.date.setText(f"Started at: {self.taskData['startDate']}")
                self.date.setVisible(True)
            else:
                self.date.setVisible(False)
        
        self.layout.update()

    def changeState(self, state):
        stateMap: Dict = {
            Qt.Unchecked: "NotStarted",
            Qt.PartiallyChecked: "InProgress",
            Qt.Checked: "Completed"
        }

        match state:
            case Qt.PartiallyChecked:
                self.taskData["startDate"] = QDate.currentDate().toString("yyyy-MM-dd")
            case Qt.Checked:
                self.taskData["completionDate"] = QDate.currentDate().toString("yyyy-MM-dd")

        newState: str = stateMap.get(state, "NotStarted")

        completionDate = self.taskData["completionDate"] if "completionDate" in self.taskData else None

        self.dbManager.executeQuery(
            "UPDATE Task SET state = ?, startDate = ?, completionDate = ? WHERE id = ?",
            [newState, self.taskData["startDate"], completionDate, self.taskData["id"]]
        )

        self.taskData["state"] = state

        self._updateDateLabel()
        
    def edit(self):
        dialog = TaskDialog(self.taskData)
        result: int = dialog.exec()
        if result == QDialog.DialogCode.Accepted:
            name: str = dialog.resultName
            description: str = dialog.resultDescription
            self.taskData["name"]: str = name
            self.taskData["description"]: str = description
            self.task.setText(name)
            doc = QTextDocument()
            doc.setMarkdown(description)
            self.parent().description.setText(doc.toHtml())

            self.dbManager.executeQuery(
                "UPDATE Task SET name = ?, description = ? WHERE id = ?",
                [name, description, self.taskData["id"]]
            )

    def delete(self):
        from UI.Project.Task import Task
        from UI.Project.Phase import Phase

        confirmation = QMessageBox.question(self, "Delete task",
                                    f"Delete task {self.taskData['name']}? It will be permanently lost!",
                                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if confirmation == QMessageBox.Yes:
            taskWidget: Task = self.parent()

            if hasattr(taskWidget.parent(), "subtasks"):
                parentTask: Task = taskWidget.parent()
                parentTask.subtasks.remove(taskWidget)
                parentTask.subtasksLayout.removeWidget(taskWidget)
                taskWidget.deleteLater()
            else:
                phaseWidget: Phase = taskWidget.parent().parent().parent().parent()
                if hasattr(phaseWidget, "phaseData") and "tasks" in phaseWidget.phaseData:
                    phaseWidget.phaseData["tasks"].remove(taskWidget.taskData)

                for i in range(phaseWidget.tasksLayout.count()):
                    if phaseWidget.tasksLayout.itemAt(i).widget() == taskWidget:
                        phaseWidget.tasksLayout.removeWidget(taskWidget)
                        taskWidget.deleteLater()
                        break
                    
            self.dbManager.executeQuery("DELETE FROM Task WHERE id = ?", [self.taskData["id"]])

    def moveUp(self):
        from UI.Project.Task import Task

        taskWidget: Task = self.parent()
        layout: QVBoxLayout = None

        if hasattr(taskWidget.parent(), "subtasksLayout"):
            layout = taskWidget.parent().subtasksLayout
        else:
            layout = taskWidget.parent().parent().parent().parent().tasksLayout

        currentIndex: int = -1
        for i in range(layout.count()):
            if layout.itemAt(i).widget() == taskWidget:
                currentIndex = i
                break
            
        if currentIndex > 0:
            prevWidget: Task = layout.itemAt(currentIndex - 1).widget()

            layout.removeWidget(taskWidget)
            layout.insertWidget(currentIndex - 1, taskWidget)

            query, _ = self.dbManager.executeQuery(
                "SELECT position FROM Task WHERE id = ?",
                [self.taskData["id"]]
            )
            query.next()
            oldPosition: int = query.value("position")

            query, _ = self.dbManager.executeQuery(
                "SELECT position FROM Task WHERE id = ?",
                [prevWidget.taskData["id"]]
            )
            query.next()
            swapPosition: int = query.value("position")

            operations: List[Set[str, List[int]]] = [
                ["UPDATE Task SET position = ? WHERE id = ?", [swapPosition, self.taskData["id"]]],
                ["UPDATE Task SET position = ? WHERE id = ?", [oldPosition, prevWidget.taskData["id"]]]
            ]

            self.dbManager.executeTransaction(operations)

    def moveDown(self):
        from UI.Project.Task import Task

        taskWidget: Task = self.parent()
        layout: QVBoxLayout = None

        if hasattr(taskWidget.parent(), "subtasksLayout"):
            layout = taskWidget.parent().subtasksLayout
        else:
            layout = taskWidget.parent().parent().parent().parent().tasksLayout

        currentIndex: int = -1
        for i in range(layout.count()):
            if layout.itemAt(i).widget() == taskWidget:
                currentIndex = i
                break
            
        if currentIndex < layout.count() - 1:
            nextWidget: Task = layout.itemAt(currentIndex + 1).widget()

            layout.removeWidget(taskWidget)
            layout.insertWidget(currentIndex + 1, taskWidget)

            query, _ = self.dbManager.executeQuery(
                "SELECT position FROM Task WHERE id = ?",
                [self.taskData["id"]]
            )
            query.next()
            oldPosition: int = query.value("position")

            query, _ = self.dbManager.executeQuery(
                "SELECT position FROM Task WHERE id = ?",
                [nextWidget.taskData["id"]]
            )
            query.next()
            swapPosition: int = query.value("position")

            operations: List[Set[str, List[int]]] = [
                ["UPDATE Task SET position = ? WHERE id = ?", [swapPosition, self.taskData["id"]]],
                ["UPDATE Task SET position = ? WHERE id = ?", [oldPosition, nextWidget.taskData["id"]]]
            ]

            self.dbManager.executeTransaction(operations)

    def addSubtask(self):
        from UI.Project.Task import Task

        dialog = TaskDialog()
        result: int = dialog.exec()
        if result == QDialog.DialogCode.Accepted:
            name: str = dialog.resultName
            description: str = dialog.resultDescription
            doc = QTextDocument()
            doc.setMarkdown(description)

            query, success = self.dbManager.executeQuery(
                "SELECT phaseId FROM Task WHERE id = ?",
                [self.taskData["id"]]
            )
            
            if not success or not query.next():
                print("ERROR: Could not find parent task to determine phaseId")
                return

            phaseId: int = query.value("phaseId")
            if phaseId is None:
                print("ERROR: Parent task has no phaseId")
                return

            _, success = self.dbManager.executeQuery(
                """
                INSERT INTO Task (name, description, phaseId, parentTaskId)
                VALUES (?, ?, ?, ?)
                """,
                [name, description, phaseId, self.taskData["id"]]
            )
            
            if not success:
                print("ERROR: Failed to insert subtask")
                return

            if success:
                query, _ = self.dbManager.executeQuery("SELECT MAX(id) AS max_id FROM Task")
                query.next()
                maxId: int = query.value("max_id")
                
                newSubtaskData: Dict = {
                    "id": maxId,
                    "name": name,
                    "description": doc.toHtml(),
                    "artifactTemplates": [],
                    "artifacts": [],
                    "state": Qt.Unchecked,
                    "subtasks": []
                }
    
                newSubtask = Task(newSubtaskData, self.dbManager)
                self.parent().subtasksLayout.addWidget(newSubtask)
                newSubtask.setVisible(self.parent().expanded)
                self.parent().subtasks.append(newSubtask)

                query, _ = self.dbManager.executeQuery(
                    "SELECT MAX(position) FROM Task WHERE parentTaskId = ?",
                    [self.taskData["id"]]
                )
                query.next()
                maxPosition: int = query.value(0)
                newPosition: int = (maxPosition + 1) if maxPosition is not None else 0

                self.dbManager.executeQuery(
                    "UPDATE Task SET position = ? WHERE id = ?",
                    [newPosition, maxId]
                )