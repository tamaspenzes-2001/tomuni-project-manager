from PySide6.QtWidgets import QWidget, QLabel, QPushButton, QHBoxLayout, QMainWindow
from PySide6.QtCore import QDate
import qtawesome as qta
from UI.Sidebar.FinishedProjectsMenuEntry import FinishedProjectsMenuEntry
from DataManager.DatabaseManager import DatabaseManager

class InProgressProjectsMenuEntry(QWidget):
    def __init__(self, name: str, id: int, dbManager: DatabaseManager):
        super().__init__()
        self.dbManager = dbManager
        self.id = id

        self.name = QLabel(name)
        self.completeButton = QPushButton()
        self.completeButton.setIcon(qta.icon("fa5s.check"))

        self.layout = QHBoxLayout()
        self.layout.addWidget(self.name)
        self.layout.addWidget(self.completeButton)
        self.setLayout(self.layout)

        self.mouseReleaseEvent = self.openProject
        self.completeButton.clicked.connect(self.completeProject)

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

        projectData = {
            "name": projectQuery.value("name"),
            "startDate": projectQuery.value("startDate"),
            "finishDate":projectQuery.value("finishDate"),
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
            ORDER BY ph.position
            """,
            [self.id]
        )

        while phasesQuery.next():
            phaseData = {
                "id": phasesQuery.value("id"),
                "name": phasesQuery.value("name"),
                "tasks": []
            }

            tasksQuery, _ = self.dbManager.executeQuery(
                """
                SELECT t.id, t.name, t.description, t.state, t.startDate, t.completionDate, t.parentTaskId
                FROM Task t
                WHERE t.phaseId = ? AND t.parentTaskId IS NULL
                ORDER BY t.id
                """,
                [phasesQuery.value("id")]
            )

            while tasksQuery.next():
                taskData = {
                    "name": tasksQuery.value("name"),
                    "description": tasksQuery.value("description") or "",
                    "state": tasksQuery.value("state"),
                    "startDate": tasksQuery.value("startDate"),
                    "completionDate": tasksQuery.value("completionDate"),
                    "artifactTemplates": [],
                    "artifacts": [],
                    "subtasks": []
                }

                artifactQuery, _ = self.dbManager.executeQuery(
                    """
                    SELECT filePath, template
                    FROM Artifact
                    WHERE taskId = ?
                    """,
                    [tasksQuery.value("id")]
                )

                while artifactQuery.next():
                    if artifactQuery.value("template"):
                        taskData["artifactTemplates"].append(artifactQuery.value("filePath"))
                    else:
                        taskData["artifacts"].append(artifactQuery.value("filePath"))

                subtasksQuery, _ = self.dbManager.executeQuery(
                    """
                    SELECT t.id, t.name, t.description, t.state, t.startDate, t.completionDate
                    FROM Task t
                    WHERE t.parentTaskId = ?
                    ORDER BY t.id
                    """,
                    [tasksQuery.value("id")]
                )

                while subtasksQuery.next():
                    subtaskData = {
                        "name": subtasksQuery.value("name"),
                        "description": subtasksQuery.value("description") or "",
                        "state": subtasksQuery.value("state"),
                        "startDate": subtasksQuery.value("startDate"),
                        "completionDate": subtasksQuery.value("completionDate"),
                        "artifactTemplates": [],
                        "artifacts": [],
                        "subtasks": []
                    }

                    subtaskArtifactQuery, _ = self.dbManager.executeQuery(
                        """
                        SELECT filePath, template
                        FROM Artifact
                        WHERE taskId = ?
                        """,
                        [subtasksQuery.value("id")]
                    )

                    while subtaskArtifactQuery.next():
                        if subtaskArtifactQuery.value("template"):
                            subtaskData["artifactTemplates"].append(subtaskArtifactQuery.value("filePath"))
                        else:
                            subtaskData["artifacts"].append(subtaskArtifactQuery.value("filePath"))

                    taskData["subtasks"].append(subtaskData)

                phaseData["tasks"].append(taskData)

            projectData["phases"].append(phaseData)

        try:
            mainWindow = self
            while mainWindow and not isinstance(mainWindow, QMainWindow):
                mainWindow = mainWindow.parent()

            if mainWindow and hasattr(mainWindow, 'loadProject'):
                mainWindow._currentProjectMenuEntry = self
                mainWindow.loadProject(projectData)
        except Exception as e:
            print(f"Error opening project: {e}")

    def completeProject(self):
        projectsSection = self.parent().parent().parent().parent().parent().parent().parent()
        finishedProjectsMenuLayout = projectsSection.finishedProjectsTab.menuLayout
        finishedProject = FinishedProjectsMenuEntry(self.name.text(), self.id, self.dbManager)
        finishedProjectsMenuLayout.insertWidget(0, finishedProject)
        self.deleteLater()

        self.dbManager.executeQuery(
            "UPDATE Project SET state = ?, finishDate = ? WHERE id = ?",
            ["Finished", QDate.currentDate().toString("yyyy-MM-dd"), self.id]
        )
