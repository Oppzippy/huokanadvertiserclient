import json
from pathlib import Path
from rx.subject.behaviorsubject import BehaviorSubject


class Configuration:
    def __init__(self, file_path: str):
        self._file_path = file_path
        self._create_config_file()
        self._modified_settings = {}
        self.api_base_url = "http://localhost:5001"

        self.api_key = BehaviorSubject(None)
        self.api_key.subscribe(on_next=lambda api_key: self._set("apiKey", api_key))
        self.wow_path = BehaviorSubject(
            "C:\\Program Files (x86)\\World of Warcraft\\_retail_"
        )
        self.wow_path.subscribe(on_next=lambda wow_path: self._set("wowPath", wow_path))

        self._load()

    def _create_config_file(self):
        path = Path(self._file_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.touch(exist_ok=True)

    def _set(self, key: str, value):
        if value is not None:
            self._modified_settings[key] = value
        elif key in self._modified_settings:
            del self._modified_settings[key]

    def _load(self) -> None:
        with open(self._file_path, "r") as f:
            try:
                config = json.loads(f.read())
                if "apiKey" in config:
                    self.api_key.on_next(config["apiKey"])
                if "wowPath" in config:
                    self.wow_path.on_next(config["wowPath"])
            except json.decoder.JSONDecodeError:
                # TODO ask user if they want to wipe the file
                pass

    def save(self) -> None:
        with open(self._file_path, "w") as f:
            f.write(json.dumps(self._modified_settings))
