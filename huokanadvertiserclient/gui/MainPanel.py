from typing import Union

from huokanapiclient.client import AuthenticatedClient

from huokanadvertiserclient.gui.framework.PanelSwitcher import PanelSwitcher
from huokanadvertiserclient.gui.framework.ReactivePanel import ReactivePanel
from huokanadvertiserclient.gui.LoggedIn import LoggedIn
from huokanadvertiserclient.gui.Login import Login
from huokanadvertiserclient.state.State import State


class MainPanel(ReactivePanel, PanelSwitcher):
    def __init__(self, parent, state: State):
        super().__init__(parent)
        self._state = state
        self._login: Union[Login, None] = None
        self._modules: Union[LoggedIn, None] = None
        self.bind_observable(state.api_client, self._on_api_client_change)

    def _on_api_client_change(self, api_client: Union[AuthenticatedClient, None]):
        if self._login is not None and api_client is None:
            return
        if api_client is None:
            self.set_panel(Login(self, self._state))
        else:
            self.set_panel(LoggedIn(self, self._state))
