from PySide6.QtWidgets import (QWidget, QCheckBox, QLabel, QToolButton, QMenu, QSizePolicy,
                                QHBoxLayout, QVBoxLayout, QMessageBox, QDialog)
from PySide6.QtGui import QAction, QTextDocument
from PySide6.QtCore import Qt, QDate
import qtawesome as qta
from typing import Dict
from UI.Dialogs.TaskDialog import TaskDialog
from DataManager.DatabaseManager import DatabaseManager
from DataManager.ConfigManager import ConfigManager

class TaskHeader(QWidget):
    def __init__(self, taskData: Dict, dbManager: DatabaseManager, confManager: ConfigManager):
        super().__init__()
        self.taskData: Dict = taskData
        self.dbManager: DatabaseManager = dbManager
        self.confManager: ConfigManager = confManager
        self.expanded: bool = False

        self.expandCollapseButton = QToolButton()
        self.expandCollapseButton.setIcon(qta.icon("fa5s.chevron-right"))
        self.expandCollapseButton.clicked.connect(self.expandCollapse)

        self.task = QCheckBox(taskData["name"])
        self.task.setTristate()
        self.task.setCheckState(taskData["state"])
        self.task.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self._setBoldCheckboxText()

        _originalMousePress = self.task.mousePressEvent

        def _customMousePress(event):
            if self.task.checkState() == Qt.Checked:
                return
            _originalMousePress(event)

        self.task.mousePressEvent = _customMousePress

        self.task.checkStateChanged.connect(self.changeState)

        self.date = QLabel("")

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

        self.layout = QHBoxLayout()
        self.layout.addWidget(self.expandCollapseButton)
        self.layout.addWidget(self.task)
        self.layout.addStretch()
        self.layout.addWidget(self.date)
        self.layout.addWidget(self.menuButton)
        self.setLayout(self.layout)

    # OVERRIDDEN METHODS

    def sizeHint(self):
        # Calculate the width required for the text + checkbox + date + icons
        text = self.task.text()
        text_width = self.task.fontMetrics().horizontalAdvance(text)
        
        checkbox_width = self.task.sizeHint().width()
        date_width = self.date.fontMetrics().horizontalAdvance(self.date.text()) if self.date.isVisible() else 0
        
        # Add padding for buttons and margins
        total_width = text_width + checkbox_width + date_width
        
        # Return a hint that is definitely wide enough
        hint = super().sizeHint()
        hint.setWidth(max(hint.width(), total_width, 350)) # Increased minimum to 350
        
        return hint

    def minimumSizeHint(self):
        # Same logic as sizeHint but for minimums
        text = self.task.text()
        text_width = self.task.fontMetrics().horizontalAdvance(text)
        checkbox_width = self.task.minimumSizeHint().width()
        date_width = self.date.fontMetrics().horizontalAdvance(self.date.text()) if self.date.isVisible() else 0
        
        min_width = text_width + checkbox_width + date_width
        hint = super().minimumSizeHint()
        hint.setWidth(max(hint.width(), min_width, 350))
        
        return hint

    def _updateContainerWidth(self):
        taskWidget: Task = self.parent()

        if hasattr(taskWidget.parent(), "subtasks"):
            widgetToUpdate: Task = taskWidget.parent()
        else:
            widgetToUpdate: Phase = taskWidget.parent().parent().parent().parent()
        
        widgetToUpdate.updateGeometry()
        widgetToUpdate.update()

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

        if self.parent():
            self.parent().updateGeometry()
            if hasattr(self.parent(), 'parent') and self.parent().parent():
                self.parent().parent().updateGeometry()

        self._setBoldCheckboxText()

        self._updateContainerWidth()

    # HELPERS

    def _setBoldCheckboxText(self):
        currentFont = self.task.font()
        if self.task.checkState() == Qt.PartiallyChecked:
            currentFont.setBold(True)
        else:
            currentFont.setBold(False)
        self.task.setFont(currentFont)

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
        
        # self.layout.update()

        if self.parent():
            self.parent().updateGeometry()
            self.parent().parent().updateGeometry()

    # SLOTS

    def expandCollapse(self):
        from UI.Project.Project import Project

        self.expanded = not self.expanded
        self.parent().description.setVisible(self.expanded)
        self.parent().artifactTemplates.setVisible(self.expanded)
        self.parent().artifacts.setVisible(self.expanded)
        for subtask in self.parent().subtasks:
            subtask.setVisible(self.expanded)
        icon: str = "fa5s.chevron-down" if self.expanded else "fa5s.chevron-right"
        self.expandCollapseButton.setIcon(qta.icon(icon))

        current_widget = self.parent() # This is the Task widget
        while current_widget:
            current_widget.updateGeometry()
            current_widget.update()

            # If we hit the Project widget, we are done
            if isinstance(current_widget, Project):
                break

            current_widget = current_widget.parent()

        # 4. Force the Project's layout to recalculate immediately
        # This is the missing link: telling the Grid Layout to ignore cached sizes
        if hasattr(self.parent(), 'parent'):
            phase_widget = self.parent().parent()
            if hasattr(phase_widget, 'parent'):
                project_widget = phase_widget.parent()
                if isinstance(project_widget, Project):
                    # Force the scroll area to recalculate its contents
                    project_widget.scrollArea.updateGeometry()
                    project_widget.updateGeometry()
                    project_widget.update()

                    # Force the grid layout to recalculate columns
                    project_widget.phasesLayout.activate()
        
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

            self._updateContainerWidth()

    def delete(self):
        from UI.Project.Task import Task
        from UI.Project.Phase import Phase

        if self.confManager.config["delConfirmTasks"]:
            confirmation = QMessageBox.question(self, "Delete task",
                                        f"Delete task {self.taskData['name']}? It will be permanently lost!",
                                        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            confirmed = confirmation == QMessageBox.Yes
        else:
            confirmed = True
        if confirmed:
            taskWidget: Task = self.parent()

            if hasattr(taskWidget.parent(), "subtasks"):
                parentTask: Task = taskWidget.parent()
                parentTask.subtasks.remove(taskWidget)
                parentTask.taskBodyLayout.removeWidget(taskWidget)
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

            self._updateContainerWidth()
                    
            self.dbManager.executeQuery("DELETE FROM Task WHERE id = ?", [self.taskData["id"]])

    def moveUp(self):
        from UI.Project.Task import Task

        taskWidget: Task = self.parent()
        layout: QVBoxLayout = None

        if hasattr(taskWidget.parent(), "taskBodyLayout"):
            layout = taskWidget.parent().taskBodyLayout
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

        if hasattr(taskWidget.parent(), "taskBodyLayout"):
            layout = taskWidget.parent().taskBodyLayout
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
    
                newSubtask = Task(newSubtaskData, self.dbManager, self.confManager)
                self.parent().taskBodyLayout.addWidget(newSubtask)
                newSubtask.setVisible(self.expanded)
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
            
            self._updateContainerWidth()