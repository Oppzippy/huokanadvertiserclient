import wx
import rx
from huokanadvertiserclient.config.Configuration import Configuration
from huokanadvertiserclient.gui.AddOn import AddOn
from huokanadvertiserclient.gui.Settings import Settings
from huokanadvertiserclient.gui.Version import Version


class Modules(wx.Panel):
    def __init__(self, parent, config: Configuration):
        super().__init__(parent)

        sizer = wx.BoxSizer(wx.VERTICAL)
        self._notebook = wx.Notebook(self)
        self._settings = Settings(self._notebook, config)

        self._notebook.AddPage(self._settings, "Settings")
        self._notebook.AddPage(AddOn(self._notebook, config.wow_path), "AddOn")
        # self._notebook.AddPage(
        #     GuildBank(self._notebook, ),
        #     "Guild Bank",
        # )
        self._notebook.AddPage(Version(self._notebook, rx.empty()), "Version")

        sizer.Add(self._notebook, flag=wx.EXPAND)
        self.SetSizer(sizer)
