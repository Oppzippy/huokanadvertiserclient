from typing import Union
import wx
from huokanadvertiserclient.config.Configuration import Configuration
from huokanadvertiserclient.gui.Login import Login
from huokanadvertiserclient.gui.Modules import Modules
from huokanadvertiserclient.gui.SystemTrayIcon import SystemTrayIcon


class RootFrame(wx.Frame):
    def __init__(self, config: Configuration):
        super().__init__(parent=None, title="Huokan Client")
        self._config = config
        self._login: Union[Login, None] = None
        self._modules: Union[Modules, None] = None
        config.api_key.subscribe(on_next=self._on_api_key_change)
        self.Bind(wx.EVT_ICONIZE, self._on_minimize)
        self.Bind(wx.EVT_WINDOW_DESTROY, self._on_destroy)

        self._system_tray_icon = SystemTrayIcon(self)

    def _on_api_key_change(self, api_key: Union[str, None]):
        if self._login is not None and api_key is None:
            return
        self.DestroyChildren()
        self._login = None
        self._modules = None

        sizer = wx.BoxSizer(wx.VERTICAL)

        if api_key is None:
            self._login = Login(self, self._config)
            sizer.Add(self._login, proportion=1, flag=wx.EXPAND)
        else:
            self._modules = Modules(self, self._config)
            sizer.Add(self._modules, proportion=1, flag=wx.EXPAND)
        self.SetSizer(sizer)

    def _on_minimize(self, _) -> None:
        if self.IsIconized():
            self.Hide()

    def _on_destroy(self, _) -> None:
        self._system_tray_icon.Destroy()
