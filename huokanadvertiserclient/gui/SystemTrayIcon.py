import wx
import wx.adv

from huokanadvertiserclient.resources import get_resource_path


class SystemTrayIcon(wx.adv.TaskBarIcon):
    def __init__(self, rootFrame: wx.Frame):
        super().__init__()
        self._frame = rootFrame
        self.SetIcon(wx.Icon(get_resource_path("huokan.ico")))
        self.Bind(wx.adv.EVT_TASKBAR_LEFT_DCLICK, self._show_frame)

    def _show_frame(self, _) -> None:
        if not self._frame.IsShown():
            self._frame.Show()
            self._frame.Iconize(False)
        else:
            self._frame.Raise()

    def CreatePopupMenu(self) -> wx.Menu:
        menu = wx.Menu()
        item = wx.MenuItem(menu, -1, "Exit")
        menu.Bind(wx.EVT_MENU, self._exit, id=item.GetId())
        menu.Append(item)
        return menu

    def _exit(self, _) -> None:
        self._frame.Destroy()
