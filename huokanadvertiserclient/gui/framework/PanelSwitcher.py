from typing import Union

import wx


class PanelSwitcher(wx.Panel):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self._active_panel: Union[wx.Panel, None] = None
        self._sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self._sizer)

    # panel must be a child of self
    def set_panel(self, panel: wx.Panel):
        if self._active_panel is not None:
            self._active_panel.Destroy()
        self._sizer.Clear()
        self._active_panel = panel
        self._sizer.Add(self._active_panel, proportion=1, flag=wx.EXPAND)
        self.Layout()
        self.Refresh()
