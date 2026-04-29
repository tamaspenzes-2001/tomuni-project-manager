from PySide6.QtWidgets import QMainWindow, QSplitter
from PySide6.QtCore import Qt
from datetime import date
from UI.Sidebar.Sidebar import Sidebar
from UI.Project.Project import Project

class AppUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.sidebar = Sidebar()
        self.project = Project({
            "name": "Todo app",
            "date": "2026-04-23",
            "phases": [{
                "name": "Plan",
                "tasks": [{
                    "name": "Define objectives",
                    "description": "What **values** should the software represent?",
                    "artifactTemplates": [],
                    "artifacts": ["/home/work/Documents/todo/objectives.txt"],
                    "state": Qt.Checked,
                    "startDate": date(2026, 1, 10),
                    "completionDate": date(2026, 1, 11),
                    "subtasks": []
                },
                {
                    "name": "Document functional requirements",
                    "description": "All the *things* **users interact** with.",
                    "artifactTemplates": ["~/Documents/requirements-spec-template.docx"],
                    "artifacts": ["~/Documents/todo-app/user-stories.txt", "~/Documents/todo-app/requirements-spec.docx"],
                    "state": Qt.PartiallyChecked,
                    "startDate": date(2026, 1, 16),
                    "subtasks": [{
                        "name": "Features",
                        "description": "",
                        "artifactTemplates": [],
                        "artifacts": [],
                        "state": Qt.Checked,
                        "startDate": date(2026, 1, 16),
                        "completionDate": date(2026, 1, 18),
                        "subtasks": []
                    },
                    {
                        "name": "Inputs",
                        "description": "",
                        "artifactTemplates": [],
                        "artifacts": [],
                        "state": Qt.PartiallyChecked,
                        "startDate": date(2026, 1, 18),
                        "subtasks": []
                    }]
                }]
            },
            {
                "name": "Implement",
                "tasks": [{
                    "name": "Frontend development",
                    "description": "The things users can see",
                    "artifactTemplates": [],
                    "artifacts": ["~/Documents/todo-app/ui-design.png"],
                    "state": Qt.Unchecked,
                    "subtasks": []
                },
                {
                    "name": "Backend development",
                    "description": "All the functionality, data storage.",
                    "artifactTemplates": [],
                    "artifacts": [],
                    "state": Qt.Unchecked,
                    "subtasks": []
                }]
            }]
        })

        self.splitter = QSplitter()
        self.splitter.addWidget(self.sidebar)
        self.splitter.addWidget(self.project)
        self.splitter.setCollapsible(1, False)
        self.setCentralWidget(self.splitter)