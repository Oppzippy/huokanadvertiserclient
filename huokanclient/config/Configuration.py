import json
from pathlib import Path
import os


class Configuration:
    def __init__(self, file_path: str):
        self._file_path = file_path
        self._config: dict

        path = Path(file_path)
        path.parent.mkdir(parents=True)
        path.touch(exist_ok=True)

        self.reload()

    def reload(self) -> None:
        with open(self._file_path, "r") as f:
            try:
                self._config = json.loads(f.read())
            except json.decoder.JSONDecodeError:
                self._config = {}

    def save(self) -> None:
        with open(self._file_path, "w") as f:
            f.write(json.dumps(self._config))

    def get_wow_path(self) -> str:
        return self._config.get(
            "wow_path", "C:\\Program Files (x86)\\World of Warcraft\\_retail_"
        )
