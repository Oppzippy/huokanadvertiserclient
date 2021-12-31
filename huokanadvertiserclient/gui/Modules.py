import wx
from huokanadvertiserclient.config.Configuration import Configuration
from huokanadvertiserclient.gui.AddOn import AddOn
from huokanadvertiserclient.gui.Settings import Settings


class Modules(wx.Panel):
    def __init__(self, parent, config: Configuration):
        super().__init__(parent)

        sizer = wx.BoxSizer(wx.VERTICAL)
        self._notebook = wx.Notebook(self)
        self._settings = Settings(self._notebook, config)

        self._notebook.AddPage(self._settings, "Settings")
        self._notebook.AddPage(
            AddOn(self._notebook, self._settings.get_wow_path_observable()), "AddOn"
        )
        # self._notebook.AddPage(
        #     GuildBank(self._notebook, ),
        #     "Guild Bank",
        # )

        sizer.Add(self._notebook, flag=wx.EXPAND)
        self.SetSizer(sizer)
