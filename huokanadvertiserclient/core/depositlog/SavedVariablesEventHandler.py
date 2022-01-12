from typing import Union
from rx.core.typing import Observer
from watchdog.events import (
    DirCreatedEvent,
    DirModifiedEvent,
    FileCreatedEvent,
    FileModifiedEvent,
    FileSystemEventHandler,
)
from pathlib import Path


class SavedVariablesEventHandler(FileSystemEventHandler):
    def __init__(self, observer: Observer) -> None:
        super().__init__()
        self._observer = observer

    def on_created(self, event: Union[DirCreatedEvent, FileCreatedEvent]) -> None:
        if isinstance(event, FileCreatedEvent):
            self._on_update(event)

    def on_modified(self, event: Union[DirModifiedEvent, FileModifiedEvent]) -> None:
        if isinstance(event, FileModifiedEvent):
            self._on_update(event)

    def _on_update(self, event: Union[FileCreatedEvent, FileModifiedEvent]) -> None:
        path = Path(event.src_path)
        if path.name == "HuokanAdvertiserTools.lua":
            self._observer.on_next(path)
