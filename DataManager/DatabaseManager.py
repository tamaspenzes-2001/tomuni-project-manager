from PySide6.QtSql import QSqlDatabase, QSqlQuery
from typing import List, Dict, Tuple
import helpers

class DatabaseManager:
    def __init__(self, encryptionEnabled: bool = False):
        self.dbPath: str = helpers.dataPath("data.db")
        self.db = QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName(self.dbPath)
        self.db.open()

        if not self.db.tables():
            self._createTables_()

    def _createTables_(self):
        self.executeQuery("PRAGMA foreign_keys = ON")

        tableData: List[Dict] = [{
            "name": "Project",
            "fields":
                """
                name VARCHAR NOT NULL, 
                state VARCHAR NOT NULL DEFAULT 'InProgress',
                startDate VARCHAR NOT NULL,
                finishDate VARCHAR,
                template BOOLEAN NOT NULL DEFAULT 0
                """
        },
        {
            "name": "Phase",
            "fields":
                """
                name VARCHAR NOT NULL,
                projectId INT NOT NULL,
                position INT NOT NULL DEFAULT 0,
                """,
            "foreignKeys": [
                ["projectId", "Project"]
            ]
        },
        {
            "name": "Task",
            "fields":
                """
                name VARCHAR NOT NULL,
                description VARCHAR,
                phaseId INT,
                parentTaskId INT,
                state VARCHAR NOT NULL DEFAULT 'NotStarted',
                startDate VARCHAR,
                completionDate VARCHAR,
                """,
            "foreignKeys": [
                ["phaseId", "Phase"],
                ["parentTaskId", "Task"]
            ]
        },
        {
            "name": "Artifact",
            "fields":
                """
                filePath VARCHAR NOT NULL,
                template BOOLEAN NOT NULL DEFAULT 0,
                taskId INT NOT NULL,
                """,
            "foreignKeys": [
                ["taskId", "Task"]
            ]
        }]

        operations = []
        for table in tableData:
            foreignKeys: str = ""
            if "foreignKeys" in table:
                for fk in table["foreignKeys"]:
                    foreignKeys += f"FOREIGN KEY({fk[0]}) REFERENCES {fk[1]}(id),\n"
            sql: str = f"""
            CREATE TABLE IF NOT EXISTS {table["name"]} (
                id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
                {table["fields"]}
                {foreignKeys.strip(",\n")}
            )
            """
            operations.append((sql, []))
        self.executeTransaction(operations)

    def executeQuery(self, queryString: str, parameters: List = [],
            query: QSqlQuery = None) -> Tuple[QSqlQuery, bool]:
        if query is None:
            query = QSqlQuery(self.db)
        query.prepare(queryString)
        for param in parameters:
            query.addBindValue(str(param))
        if not query.exec():
            print(f"Failed to execute query: {queryString}")
            print(f"Error: {query.lastError().text()}")
            return query, False
        return query, True

    def executeTransaction(self, operations: List[Tuple[str, List]]):
        if (self.db.transaction()):
            query = QSqlQuery(self.db)
            for operation in operations:
                _, success = self.executeQuery(operation[0], operation[1], query)
                if not success:
                    self.db.rollback()
                    return
        self.db.commit()
        