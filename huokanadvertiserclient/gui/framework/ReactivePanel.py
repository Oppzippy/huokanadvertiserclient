from typing import Any, Callable, List
from rx.core.observer.observer import Observer
from rx.core.observable.observable import Observable
from rx.core.typing import Disposable
import wx


class ReactivePanel(wx.Panel):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self._observable_disposables: List[Disposable] = []

    def bind_observable(
        self, observable: Observable, set_func: Callable[[Any], None]
    ) -> None:
        disposable = observable.subscribe(on_next=set_func)
        self._observable_disposables.append(disposable)

    def bind_observer(self, observer: Observer, window: wx.Window, event) -> None:
        window.Bind(event, lambda new_value: observer.on_next(new_value))

    def Destroy(self):
        for disposable in self._observable_disposables:
            disposable.dispose()
        return super().Destroy()
