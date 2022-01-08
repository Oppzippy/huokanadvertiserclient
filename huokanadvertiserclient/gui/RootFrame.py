import wx
from huokanadvertiserclient.config.Configuration import Configuration
from huokanadvertiserclient.gui.MainPanel import MainPanel
from huokanadvertiserclient.gui.SystemTrayIcon import SystemTrayIcon


class RootFrame(wx.Frame):
    def __init__(self, config: Configuration):
        super().__init__(parent=None, title="Huokan Client")
        self._config = config
        self._system_tray_icon = SystemTrayIcon(self)

        sizer = wx.BoxSizer(wx.VERTICAL)
        self._main_panel = MainPanel(self, config)
        sizer.Add(self._main_panel, proportion=1, flag=wx.EXPAND)
        self.SetSizer(sizer)

        self.Bind(wx.EVT_ICONIZE, self._on_minimize)
        self.Bind(wx.EVT_WINDOW_DESTROY, self._on_destroy, self)

    def _on_minimize(self, _) -> None:
        if self.IsIconized():
            self.Hide()

    def _on_destroy(self, _) -> None:
        self._system_tray_icon.Destroy()
