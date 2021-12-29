import wx
from huokanclient.config.Configuration import Configuration

from huokanclient.gui.WoWDirPicker import WoWDirPicker


class RootFrame(wx.Frame):
    def __init__(self, config: Configuration):
        super().__init__(parent=None, title="Huokan Client")
        self.configuration = config

        panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)

        self.wow_path_ctrl = WoWDirPicker(panel)
        self.wow_path_ctrl.set_path(config.get_wow_path())

        sizer.Add(self.wow_path_ctrl)

        panel.SetSizer(sizer)
