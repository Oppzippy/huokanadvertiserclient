from typing import Union
import wx
from huokanadvertiserclient.config.Configuration import Configuration
from huokanadvertiserclient.gui.Login import Login
from huokanadvertiserclient.gui.Modules import Modules


class RootFrame(wx.Frame):
    def __init__(self, config: Configuration):
        super().__init__(parent=None, title="Huokan Client")
        self._config = config
        config.api_key.subscribe(on_next=self._on_api_key_change)

    def _on_api_key_change(self, api_key: Union[str, None]):
        self.DestroyChildren()
        sizer = wx.BoxSizer(wx.VERTICAL)

        if api_key is None:
            self._login = Login(self, self._config)
            sizer.Add(self._login, flag=wx.EXPAND)
        else:
            self._modules = Modules(self, self._config)
            sizer.Add(self._modules, flag=wx.EXPAND)
        self.SetSizer(sizer)
