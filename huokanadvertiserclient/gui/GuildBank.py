import wx
from datetime import datetime

from rx.core.observable.observable import Observable


class GuildBank(wx.Panel):
    def __init__(self, parent, guild_bank_upload: Observable):
        super().__init__(parent)

        sizer = wx.BoxSizer(wx.VERTICAL)
        self._last_upload = wx.StaticText(self)

        sizer.Add(self._last_upload, flag=wx.EXPAND)
        self.SetSizer(sizer)
        guild_bank_upload.subscribe(on_next=self._update_last_upload)

    def _update_last_upload(self, _) -> None:
        now = datetime.now()
        self._last_upload.SetLabel(now.strftime("%x %X"))
