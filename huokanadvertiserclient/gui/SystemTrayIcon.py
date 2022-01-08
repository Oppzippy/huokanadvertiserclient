import wx
import wx.adv


class SystemTrayIcon(wx.adv.TaskBarIcon):
    def __init__(self, rootFrame: wx.Frame):
        super().__init__()
        self._frame = rootFrame
        self.Bind(wx.adv.EVT_TASKBAR_LEFT_DCLICK, self._show_frame)

    def _show_frame(self, _) -> None:
        self._frame.Show()
