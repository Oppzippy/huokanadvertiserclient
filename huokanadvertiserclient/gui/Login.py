import webbrowser
from typing import Union

import wx

from huokanadvertiserclient.core.discord.OAuthListener import OAuthListener
from huokanadvertiserclient.gui.framework.ReactivePanel import ReactivePanel
from huokanadvertiserclient.state.State import State


class Login(ReactivePanel):
    def __init__(self, parent, state: State):
        super().__init__(parent)
        self._state = state

        sizer = wx.BoxSizer(wx.VERTICAL)

        self._button = wx.Button(self, label="Log in with Discord")
        self._button.Bind(wx.EVT_BUTTON, self._on_button_click)

        sizer.Add(self._button, proportion=1, flag=wx.EXPAND)
        self.SetSizer(sizer)

        self._server = OAuthListener(state)
        self.Bind(wx.EVT_WINDOW_DESTROY, self._on_destroy)
        self.bind_observable(self._state.api_key, self._on_api_key_change)

    def _on_button_click(self, _) -> None:
        if self._state.api_key.value is None:
            webbrowser.open(
                f"{self._state.api_base_url.value}/authorization/discord/redirect?redirectUrl={self._server.get_redirect_url()}",
                autoraise=True,
            )
        else:
            self._state.api_key.on_next(None)

    def _on_api_key_change(self, value: Union[str, None]) -> None:
        if value is None:
            self._button.SetLabelText("Log in with Discord")
        else:
            self._button.SetLabelText("Logging in, click to cancel.")

    def _on_destroy(self, _) -> None:
        self._server.destroy()
        self._dispose_observables()
