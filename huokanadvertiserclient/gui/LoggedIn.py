import wx
import rx
from huokanadvertiserclient.state.State import State
from huokanadvertiserclient.gui.AddOn import AddOn
from huokanadvertiserclient.gui.DepositLogs import DepositLogs
from huokanadvertiserclient.gui.Settings import Settings
from huokanadvertiserclient.gui.Version import Version


class LoggedIn(wx.Panel):
    def __init__(self, parent, state: State):
        super().__init__(parent)

        sizer = wx.BoxSizer(wx.VERTICAL)
        self._notebook = wx.Notebook(self)

        self._notebook.AddPage(Settings(self._notebook, state), "Settings")
        self._notebook.AddPage(AddOn(self._notebook, state.wow_path), "AddOn")
        self._notebook.AddPage(
            DepositLogs(
                self._notebook,
                state,
            ),
            "Deposit Logs",
        )
        self._notebook.AddPage(Version(self._notebook, rx.empty()), "Version")

        sizer.Add(self._notebook, proportion=1, flag=wx.EXPAND)
        self.SetSizer(sizer)
