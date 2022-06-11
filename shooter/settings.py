from pydantic import BaseModel, Field
import os
path_to_menu = os.path.dirname(__file__)


class SettingsData(BaseModel):
    """Base class for serializations json data from settings-json-file."""
    volume: int = Field(alias="volume")
    music: int = Field(alias="music")
    language: int = Field(alias="language")


class Settings():
    """Class handler, which accumulate settings data and save this data to file."""
    def __init__(self, path: str = path_to_menu + "/menu/settings.json") -> None:
        """Init data: read settings-json-file and keep itself."""
        self.path = path
        file = open(self.path, "r")
        setting_string = file.read()
        self.data = SettingsData.parse_raw(setting_string)
        file.close()

    def save(self):
        """Function for save actual setting to settings-json-file."""
        file = open(path_to_menu + "/menu/settings.json", "w")
        file.write(self.data.json())
        file.close()
