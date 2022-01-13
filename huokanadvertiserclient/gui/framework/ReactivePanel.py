from typing import Any, Callable, List

import wx
from rx.core.observable.observable import Observable
from rx.core.observer.observer import Observer
from rx.core.typing import Disposable


class ReactivePanel(wx.Panel):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self._observable_disposables: List[Disposable] = []
        self.Bind(wx.EVT_WINDOW_DESTROY, self._dispose_observables, self)

    def bind_observable(
        self, observable: Observable, set_func: Callable[[Any], None]
    ) -> None:
        disposable = observable.subscribe(
            on_next=lambda event: wx.CallAfter(set_func, event)
        )
        self._observable_disposables.append(disposable)

    def bind_observer(
        self,
        observer: Observer,
        window: wx.Window,
        event: wx.PyEventBinder,
        get_new_value: Callable[[], Any] = None,
    ) -> None:
        window.Bind(
            event,
            lambda new_value: observer.on_next(
                new_value if get_new_value is None else get_new_value()
            ),
        )

    def _dispose_observables(self, _):
        for disposable in self._observable_disposables:
            disposable.dispose()
