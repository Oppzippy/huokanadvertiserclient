from typing import Union

from rx.core.observable.observable import Observable
from rx.core.observer.observer import Observer
from watchdog.observers import Observer as WatchdogObserver

from huokanadvertiserclient.core.depositlog.SavedVariablesEventHandler import (
    SavedVariablesEventHandler,
)


class SavedVariablesWatcher:
    def __init__(self, wow_path: Observable, observer: Observer):
        self._wow_path = wow_path
        self._file_observer: Union[WatchdogObserver, None] = None

        self._event_handler = SavedVariablesEventHandler(observer)
        self._unsubscribe = wow_path.subscribe(on_next=self._set_wow_path)

    def _set_wow_path(self, wow_path: Union[str, None]):
        if wow_path is None:
            self._destroy_file_observer()
        else:
            if self._file_observer is None:
                self._file_observer = WatchdogObserver()
            else:
                self._file_observer.unschedule_all()
            self._file_observer.schedule(self._event_handler, wow_path, recursive=True)
            if not self._file_observer.is_alive():
                self._file_observer.start()

    def destroy(self) -> None:
        self._destroy_file_observer()
        self._unsubscribe.dispose()

    def _destroy_file_observer(self) -> None:
        if self._file_observer is not None:
            self._file_observer.unschedule_all()
            self._file_observer.stop()
            self._file_observer = None
