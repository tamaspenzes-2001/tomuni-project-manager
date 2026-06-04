from PySide6.QtWidgets import QWidget, QLabel, QToolButton, QMenu, QDialog, QHBoxLayout, QMainWindow
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction
import qtawesome as qta
from typing import List, Dict
from datetime import date
from UI.Dialogs.ProjectDialog import ProjectDialog
from UI.Project.Phase import Phase
from DataManager.DatabaseManager import DatabaseManager
from DataManager.ConfigManager import ConfigManager

class ProjectHeader(QWidget):
    def __init__(self, projectData: Dict, dbManager: DatabaseManager, confManager: ConfigManager):
        super().__init__()
        self.projectData: Dict = projectData
        self.dbManager: DatabaseManager = dbManager
        self.confManager: ConfigManager = confManager

        self.name = QLabel(projectData["name"])
        self.name.setProperty("class", "heading")
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
        self.menuButton.setMenu(self.menu)

        self.projectSettingsAction = QAction("Project settings")
        self.projectSettingsAction.triggered.connect(self.modifyProjectSettings)
        self.createAction = QAction("Create a template from this project")
        self.createAction.triggered.connect(self.createTemplate)
        self.completeAction = QAction("Mark project as completed")
        self.completeAction.triggered.connect(self.markAsCompleted)

        self.menu.addAction(self.projectSettingsAction)
        self.menu.addAction(self.createAction)
        self.menu.addAction(self.completeAction)

        dateString: str = ""
        if projectData["finishDate"]:
            dateString = f"{projectData['startDate']} - {projectData['finishDate']}"
        else:
            dateString = f"Started: {projectData["startDate"]}"
        self.date = QLabel(dateString)

        self.layout = QHBoxLayout()
        self.layout.addWidget(self.name)
        self.layout.addWidget(self.menuButton)
        self.layout.addStretch()
        self.layout.addWidget(self.date)
        self.setLayout(self.layout)

    def modifyProjectSettings(self):
        dialog = ProjectDialog(data=self.projectData)
        result: int = dialog.exec()
        if result != QDialog.DialogCode.Accepted:
            return

        newName: str = dialog.resultName
        newPhaseList: List[Dict] = dialog.resultPhases

        dbOperations: List = []

        for index, phaseEntry in enumerate(newPhaseList):
            phaseId: int = phaseEntry["id"]
            phaseName: str = phaseEntry["name"]

            if phaseId is not None:
                dbOperations.append([
                    "UPDATE Phase SET name = ?, position = ? WHERE id = ?",
                    [phaseName, index, phaseId]
                ])
            else:
                dbOperations.append([
                    "INSERT INTO Phase (name, projectId, position) VALUES (?, ?, ?)",
                    [phaseName, self.projectData["id"], index]
                ])

        currentDbIds = set(self.parent().phases.keys())
        newIds: set = {p["id"] for p in newPhaseList if p["id"] is not None}

        idsToDelete: set = currentDbIds - newIds

        for phaseId in idsToDelete:
            dbOperations.append([
                "DELETE FROM Phase WHERE id = ?",
                [phaseId]
            ])

        if dbOperations:
            self.dbManager.executeTransaction(dbOperations)

        if self.name.text() != newName:
            self.name.setText(newName)
            self.dbManager.executeQuery(
                "UPDATE Project SET name = ? WHERE id = ?",
                [newName, self.projectData["id"]]
            )

        while self.parent().phasesLayout.count() > 0:
            item = self.parent().phasesLayout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        self.parent().phases.clear()

        syncQuery, success = self.dbManager.executeQuery(
            """
            SELECT ph.id AS phaseId, ph.name AS phaseName
            FROM Phase ph
            WHERE ph.projectId = ?
            ORDER BY ph.position ASC
            """,
            [self.projectData["id"]]
        )
        
        if success:
            freshPhases: List = []
            while syncQuery.next():
                dbId: int = syncQuery.value("phaseId")
                dbName: str = syncQuery.value("phaseName")
                
                if dbId is None:
                    print("ERROR: Retrieved NULL ID. Check SQL query.")
                    continue

                tasksQuery, _ = self.dbManager.executeQuery(
                    """
                    SELECT t.id, t.position, t.name, t.description, t.state, t.startDate, t.completionDate, t.phaseId, t.parentTaskId
                    FROM Task t
                    WHERE t.phaseId = ?
                    ORDER BY t.position
                    """,
                    [dbId]
                )

                tasks: List = []
                tasksById: Dict = {}
            
                while tasksQuery.next():
                    taskData: Dict = {
                        "id": tasksQuery.value("id"),
                        "name": tasksQuery.value("name"),
                        "description": tasksQuery.value("description") or "",
                        "state": self._convertState(tasksQuery.value("state")),
                        "startDate": tasksQuery.value("startDate"),
                        "completionDate": tasksQuery.value("completionDate"),
                        "parentTaskId": tasksQuery.value("parentTaskId"),
                        "position": tasksQuery.value("position"),
                        "artifactTemplates": [],
                        "artifacts": [],
                        "subtasks": []
                    }

                    tasksById[taskData["id"]] = taskData
                    tasks.append(taskData)

                rootTasks: List = []
                for task in tasks:
                    parentId: int = task["parentTaskId"]
                    if parentId is None or parentId == "" or parentId == 0:
                        rootTasks.append(task)
                    else:
                        if parentId in tasksById:
                            tasksById[parentId]["subtasks"].append(task)
                self._fetchArtifactsForTasks(tasksById.values())

                phaseData: Dict = {
                    "id": dbId,
                    "name": dbName,
                    "tasks": rootTasks 
                }

                widget = Phase(phaseData, self.dbManager, self.confManager)
                self.parent().phasesLayout.addWidget(widget)
                self.parent().phases[dbId] = widget

                freshPhases.append(phaseData)

            self.projectData["phases"] = freshPhases
            self.projectData["name"] = newName
        else:
            print("Failed to sync UI after modification.")
            print(f"Error: {self.dbManager.db.lastError().text()}")

    def _convertState(self, stateStr):
        match stateStr:
            case "NotStarted": return Qt.Unchecked
            case "InProgress": return Qt.PartiallyChecked
            case "Completed": return Qt.Checked
        return Qt.Unchecked

    def _fetchArtifactsForTasks(self, tasks):
        taskIds: List[int] = [t["id"] for t in tasks]
        if not taskIds:
            return

        placeholders: str = ",".join(["?"] * len(taskIds))
        queryStr: str = f"""
        SELECT taskId, filePath, template 
        FROM Artifact 
        WHERE taskId IN ({placeholders})
        """

        query, success = self.dbManager.executeQuery(queryStr, taskIds)
        if not success:
            return

        while query.next():
            taskId: int = query.value("taskId")
            for task in tasks:
                if task["id"] == taskId:
                    if query.value("template"):
                        task["artifactTemplates"].append(query.value("filePath"))
                    else:
                        task["artifacts"].append(query.value("filePath"))
                    break
    
    def _rebuildPhaseListFromDB(self, projectWidget, query):
        while projectWidget.phasesLayout.count() > 0:
            item: Phase = projectWidget.phasesLayout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        projectWidget.phases.clear()
        
        query, _ = self.dbManager.executeQuery(
            "SELECT id, name FROM Phase WHERE projectId = ? ORDER BY id",
            [self.projectData["id"]]
        )
        
        while query.next():
            dbId = query.value("id")
            dbName = query.value("name")

            phaseData = {
                "id": dbId,
                "name": dbName,
                "tasks": []
            }
            
            phaseWidget = Phase(phaseData, self.dbManager)
            projectWidget.phasesLayout.addWidget(phaseWidget)
            projectWidget.phases[dbId] = phaseWidget
            
    def createTemplate(self):
        pass

    def markAsCompleted(self):
        mainWindow = self
        while mainWindow and not isinstance(mainWindow, QMainWindow):
            mainWindow = mainWindow.parent()
        if mainWindow and hasattr(mainWindow, '_currentProjectMenuEntry'):
            menuEntry = mainWindow._currentProjectMenuEntry
            if hasattr(menuEntry, 'completeProject'):
                menuEntry.completeProject()
                
                if hasattr(mainWindow, 'project') and mainWindow.project:
                    mainWindow.project.deleteLater()
                    mainWindow.project = QWidget()
                    mainWindow.splitter.replaceWidget(1, mainWindow.project)

                if hasattr(mainWindow, '_currentProjectMenuEntry'):
                    delattr(mainWindow, '_currentProjectMenuEntry')