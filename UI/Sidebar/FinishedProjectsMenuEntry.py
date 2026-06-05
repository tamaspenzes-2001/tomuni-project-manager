from PySide6.QtWidgets import QWidget, QLabel, QHBoxLayout, QMainWindow
from PySide6.QtCore import Qt
from DataManager.DatabaseManager import DatabaseManager

class FinishedProjectsMenuEntry(QWidget):
    def __init__(self, name: str, id: int, dbManager: DatabaseManager):
        super().__init__()
        self.dbManager: DatabaseManager = dbManager
        self.id: int = id

        self.name = QLabel(name)
        self.layout = QHBoxLayout()
        self.layout.addWidget(self.name)
        self.setLayout(self.layout)
        self.mouseReleaseEvent = self.openProject
        self.setAttribute(Qt.WA_StyledBackground)
        self.setProperty("class", "bottom-border")

    def openProject(self, event):
        projectQuery, success = self.dbManager.executeQuery(
            """
            SELECT p.name, p.startDate, p.finishDate, p.state, p.template
            FROM Project p
            WHERE p.id = ?
            """,
            [self.id]
        )

        if not success or not projectQuery.next():
            return

        projectData: Dict = {
            "name": projectQuery.value("name"),
            "startDate": projectQuery.value("startDate"),
            "finishDate": projectQuery.value("finishDate"),
            "state": projectQuery.value("state"),
            "template": projectQuery.value("template"),
            "id": self.id,
            "phases": []
        }

        phasesQuery, _ = self.dbManager.executeQuery(
            """
            SELECT ph.id, ph.name
            FROM Phase ph
            WHERE ph.projectId = ?
            ORDER BY ph.position ASC
            """,
            [self.id]
        )

        while phasesQuery.next():
            phaseId: int = phasesQuery.value("id")
            phaseName: str = phasesQuery.value("name")

            tasksQuery, _ = self.dbManager.executeQuery(
                """
                SELECT t.id, t.name, t.description, t.state, t.startDate, t.completionDate, t.parentTaskId, t.position
                FROM Task t
                WHERE t.phaseId = ?
                ORDER BY t.position ASC
                """,
                [phaseId]
            )

            allTasks: List = []
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
                    "position": tasksQuery.value("position"), # Keep position for safety
                    "artifactTemplates": [],
                    "artifacts": [],
                    "subtasks": []
                }
                
                tasksById[taskData["id"]] = taskData
                allTasks.append(taskData)

            rootTasks: List = []

            for task in allTasks:
                parentId: int = task["parentTaskId"]
                
                if parentId is None or parentId == "" or parentId == 0:
                    rootTasks.append(task)
                else:
                    if parentId in tasksById:
                        tasksById[parentId]["subtasks"].append(task)

            self._fetchArtifactsForTasks(tasksById)

            phaseData: Dict = {
                "id": phaseId,
                "name": phaseName,
                "tasks": rootTasks
            }
            projectData["phases"].append(phaseData)

        mainWindow = self
        while mainWindow and not isinstance(mainWindow, QMainWindow):
            mainWindow = mainWindow.parent()
        if mainWindow and hasattr(mainWindow, 'loadProject'):
            mainWindow.loadProject(projectData)

    def _convertState(self, stateStr):
        match stateStr:
            case "NotStarted": return Qt.Unchecked
            case "InProgress": return Qt.PartiallyChecked
            case "Completed": return Qt.Checked
        return Qt.Unchecked

    def _fetchArtifactsForTasks(self, tasksById):
        taskIds = list(tasksById.keys())
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
            if taskId in tasksById:
                if query.value("template"):
                    section: str = "artifactTemplates"
                else:
                    section: str = "artifacts"
                tasksById[taskId][section].append(query.value("filePath"))