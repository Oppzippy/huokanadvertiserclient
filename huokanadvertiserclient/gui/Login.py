import webbrowser

import wx

from huokanadvertiserclient.core.discord.OAuthListener import OAuthListener
from huokanadvertiserclient.state.State import State


class Login(wx.Panel):
    def __init__(self, parent, state: State):
        super().__init__(parent)
        self._state = state

        sizer = wx.BoxSizer(wx.VERTICAL)

        self._login_button = wx.Button(self, label="Log in with Discord")
        self._login_button.Bind(wx.EVT_BUTTON, self._open_login_page)

        sizer.Add(self._login_button, proportion=1, flag=wx.EXPAND)
        self.SetSizer(sizer)

        self._server = OAuthListener(state)
        self.Bind(wx.EVT_WINDOW_DESTROY, lambda _: self._server.destroy())

    def _open_login_page(self, _):
        webbrowser.open(
            f"{self._state.api_base_url.value}/authorization/discord/redirect?redirectUrl={self._server.get_redirect_url()}",
            autoraise=True,
        )
