import wx
from datetime import datetime

from rx.core.observable.observable import Observable
import huokanadvertiserclient

from huokanadvertiserclient.gui.framework.ReactivePanel import ReactivePanel


class Version(ReactivePanel):
    def __init__(self, parent, latest_version_observable: Observable):
        super().__init__(parent)

        sizer = wx.BoxSizer(wx.VERTICAL)
        self._current_version = wx.StaticText(
            self, label=f"Installed Version: {huokanadvertiserclient.__version__}"
        )
        sizer.Add(self._current_version, flag=wx.EXPAND)
        self._latest_version = wx.StaticText(self)
        sizer.Add(self._latest_version, flag=wx.EXPAND)

        self.SetSizer(sizer)
        self.bind_observable(latest_version_observable, self._set_latest_version)

    def _set_latest_version(self, latest_version: str) -> None:
        self._latest_version.SetLabel(f"Latest Version: {latest_version}")
