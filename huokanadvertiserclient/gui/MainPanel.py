import wx
from typing import Union
import wx
from huokanadvertiserclient.config.Configuration import Configuration
from huokanadvertiserclient.gui.Login import Login
from huokanadvertiserclient.gui.Modules import Modules
from huokanadvertiserclient.gui.framework.PanelSwitcher import PanelSwitcher
from huokanadvertiserclient.gui.framework.ReactivePanel import ReactivePanel


class MainPanel(ReactivePanel, PanelSwitcher):
    def __init__(self, parent, config: Configuration):
        super().__init__(parent)
        self._config = config
        self._login: Union[Login, None] = None
        self._modules: Union[Modules, None] = None
        self.bind_observable(config.api_key, self._on_api_key_change)

    def _on_api_key_change(self, api_key: Union[str, None]):
        if self._login is not None and api_key is None:
            return
        if api_key is None:
            self.set_panel(Login(self, self._config))
        else:
            self.set_panel(Modules(self, self._config))
