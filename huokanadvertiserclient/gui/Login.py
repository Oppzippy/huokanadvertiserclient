import webbrowser
import wx
from huokanadvertiserclient.config.Configuration import Configuration
from huokanadvertiserclient.core.DiscordOAuthListener import DiscordOAuthListener


class Login(wx.Panel):
    def __init__(self, parent, config: Configuration):
        super().__init__(parent)
        self._config = config

        sizer = wx.BoxSizer(wx.VERTICAL)

        self._login_button = wx.Button(parent=self, label="Log in with Discord")
        self._login_button.Bind(wx.EVT_BUTTON, self._open_login_page)

        sizer.Add(self._login_button, flag=wx.EXPAND)
        self.SetSizer(sizer)

        self._server = DiscordOAuthListener(config)

    def _open_login_page(self, _):
        webbrowser.open(
            f"{self._config.api_base_url}/authorization/discord/redirect?redirectUrl={self._server.get_redirect_url()}",
            autoraise=True,
        )

    def Destroy(self):
        self._server.destroy()
        return super().Destroy()
