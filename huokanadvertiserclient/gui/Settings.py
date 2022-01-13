import wx

from huokanadvertiserclient.gui.WoWDirPicker import WoWDirPicker
from huokanadvertiserclient.state.State import State


class Settings(wx.Panel):
    def __init__(self, parent, state: State):
        super().__init__(parent)
        self._state = state

        sizer = wx.BoxSizer(wx.VERTICAL)
        self._dir_picker = WoWDirPicker(self, state.wow_path)
        sizer.Add(self._dir_picker, flag=wx.EXPAND)
        self._log_out = wx.Button(self, label="Log Out")
        self._log_out.Bind(wx.EVT_BUTTON, lambda _: state.api_key.on_next(None))
        sizer.Add(self._log_out)
        self.SetSizer(sizer)
