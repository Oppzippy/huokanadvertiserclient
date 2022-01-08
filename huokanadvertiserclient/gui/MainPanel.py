import wx
from typing import Union
import wx
from huokanadvertiserclient.config.Configuration import Configuration
from huokanadvertiserclient.gui.Login import Login
from huokanadvertiserclient.gui.Modules import Modules
from huokanadvertiserclient.gui.framework.ReactivePanel import ReactivePanel


class MainPanel(ReactivePanel):
    def __init__(self, parent, config: Configuration):
        super().__init__(parent)
        self._config = config
        self._login: Union[Login, None] = None
        self._modules: Union[Modules, None] = None
        self._sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self._sizer)
        self.bind_observable(config.api_key, self._on_api_key_change)

    def _on_api_key_change(self, api_key: Union[str, None]):
        if self._login is not None and api_key is None:
            return

        self.DestroyChildren()
        self._login = None
        self._modules = None
        self._sizer.Clear()

        if api_key is None:
            self._login = Login(self, self._config)
            self._sizer.Add(self._login, proportion=1, flag=wx.EXPAND)
        else:
            self._modules = Modules(self, self._config)
            self._sizer.Add(self._modules, proportion=1, flag=wx.EXPAND)
        self.Layout()
