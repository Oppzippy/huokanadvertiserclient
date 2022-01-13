import json
import os
from pathlib import Path

from rx.subject.behaviorsubject import BehaviorSubject
from rx.subject.subject import Subject


class State:
    def __init__(self, file_path: str):
        self._modified_settings = {}
        self._initialized = False
        self._file_path = file_path
        self._create_config_file()

        # State
        self.api_key = BehaviorSubject(None)
        self.api_base_url = BehaviorSubject(
            os.environ.get("HUOKAN_API_BASE_URL", "https://huokan.oppzippy.com/v1")
        )
        self.deposit_log_upload_status_code = Subject()

        # Config
        self.organization_id = BehaviorSubject(
            os.environ.get("HUOKAN_ORGANIZATION_ID", "TODO production organization id")
        )
        self.wow_path = BehaviorSubject(
            "C:\\Program Files (x86)\\World of Warcraft\\_retail_"
        )

        self._load()
        self.api_key.subscribe(on_next=lambda api_key: self._set("apiKey", api_key))
        self.wow_path.subscribe(on_next=lambda wow_path: self._set("wowPath", wow_path))

        self._initialized = True

    def _create_config_file(self):
        path = Path(self._file_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.touch(exist_ok=True)

    def _set(self, key: str, value):
        if value is not None:
            self._modified_settings[key] = value
        elif key in self._modified_settings:
            del self._modified_settings[key]
        if self._initialized:
            self._save()

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

    def _save(self) -> None:
        with open(self._file_path, "w") as f:
            f.write(json.dumps(self._modified_settings))
