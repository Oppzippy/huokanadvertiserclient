import wx

from huokanadvertiserclient.gui.WoWDirPicker import WoWDirPicker
from huokanadvertiserclient.config.Configuration import Configuration


class Settings(wx.Panel):
    def __init__(self, parent, config: Configuration):
        super().__init__(parent)
        self._config = config

        sizer = wx.BoxSizer(wx.VERTICAL)
        self._dir_picker = WoWDirPicker(self, config.wow_path)
        sizer.Add(self._dir_picker, flag=wx.EXPAND)
        self._log_out = wx.Button(self, label="Log Out")
        self._log_out.Bind(wx.EVT_BUTTON, lambda _: config.api_key.on_next(None))
        sizer.Add(self._log_out)
        self.SetSizer(sizer)
