from typing import Union
from huokanadvertiserclient.state.State import State
from huokanadvertiserclient.gui.Login import Login
from huokanadvertiserclient.gui.LoggedIn import LoggedIn
from huokanadvertiserclient.gui.framework.PanelSwitcher import PanelSwitcher
from huokanadvertiserclient.gui.framework.ReactivePanel import ReactivePanel


class MainPanel(ReactivePanel, PanelSwitcher):
    def __init__(self, parent, state: State):
        super().__init__(parent)
        self._state = state
        self._login: Union[Login, None] = None
        self._modules: Union[LoggedIn, None] = None
        self.bind_observable(state.api_key, self._on_api_key_change)

    def _on_api_key_change(self, api_key: Union[str, None]):
        if self._login is not None and api_key is None:
            return
        if api_key is None:
            self.set_panel(Login(self, self._state))
        else:
            self.set_panel(LoggedIn(self, self._state))
