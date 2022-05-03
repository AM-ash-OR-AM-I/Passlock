import json
from typing import List

from kivymd.app import MDApp

app = MDApp.get_running_app()


class SaveConfig:
    def __init__(self, *args: List[str]) -> None:
        self.variable_list = args
        self.variable_dict = {}

    def save_settings(self) -> None:
        for var in self.variable_list:
            exec(f"self.variable_dict['{var}']= app.{var}")
        with open("data/config.json", "w") as file:
            json.dump(self.variable_dict, file, indent=4)
