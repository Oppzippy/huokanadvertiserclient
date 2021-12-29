import wx
from huokanclient.config.Configuration import Configuration
from huokanclient.gui.Modules import Modules

from huokanclient.gui.WoWDirPicker import WoWDirPicker


class RootFrame(wx.Frame):
    def __init__(self, config: Configuration):
        super().__init__(parent=None, title="Huokan Client")
        self.configuration = config

        panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)

        self._modules = Modules(panel, config)

        sizer.Add(self._modules, flag=wx.EXPAND)

        panel.SetSizer(sizer)
