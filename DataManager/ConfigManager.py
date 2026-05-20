from helpers import dataPath
import json

class ConfigManager:
    def __init__(self):
        try:
            with open(dataPath("config.json"), "r") as config:
                self.config = json.load(config)
        except FileNotFoundError:
            self.config = {
                "delConfirmProjectTemplates": True,
                "delConfirmTasks": True,
                "dateFormat": r"%Y-%m-%d",
                "encryptionEnabled": False,
                "encryptionPassword": ""
            }
            self.saveConfig()

    def saveConfig(self):
        with open(dataPath("config.json"), "w") as config:
            json.dump(self.config, config)
