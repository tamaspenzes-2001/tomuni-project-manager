from PySide6.QtSql import QSqlDatabase, QSqlQuery
from typing import List, Dict
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
                state VARCHAR NOT NULL,
                startDate DATE NOT NULL,
                finishDate DATE,
                template BOOLEAN NOT NULL
                """
        },
        {
            "name": "Phase",
            "fields":
                """
                name VARCHAR NOT NULL,
                projectId INT NOT NULL,
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
                state VARCHAR NOT NULL,
                startDate DATE,
                completionDate DATE,
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
                template BOOLEAN NOT NULL,
                taskId INT NOT NULL,
                """,
            "foreignKeys": [
                ["taskId", "Task"]
            ]
        }]
        if (self.db.transaction()):
            query = QSqlQuery(self.db)
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

                if not query.exec(sql):
                    print(f"Failed to create table {table['name']}: {query.lastError().text()}")
                    print(f"SQL: {sql}")
                    self.db.rollback()
                    return
            self.db.commit()

    def executeQuery(self, queryString: str, parameters: List[str] = None):
        query = QSqlQuery(self.db)
        query.prepare(queryString)
        if parameters:
            for param in parameters:
                query.addBindValue(param)
        if not query.exec():
            print(f"Failed to execute query: {queryString}")
            print(f"Error: {query.lastError().text()}")
        return query