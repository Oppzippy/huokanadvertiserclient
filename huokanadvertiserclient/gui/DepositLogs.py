import wx
from datetime import datetime

from rx.core.observable.observable import Observable

from huokanadvertiserclient.gui.framework.ReactivePanel import ReactivePanel
from huokanadvertiserclient.state.State import State


class DepositLogs(ReactivePanel):
    def __init__(self, parent, state: State):
        super().__init__(parent)

        sizer = wx.BoxSizer(wx.VERTICAL)
        self._last_upload = wx.StaticText(self, label="Nothing has been uploaded yet.")

        sizer.Add(self._last_upload, flag=wx.EXPAND)
        self.SetSizer(sizer)
        self.bind_observable(
            state.deposit_log_upload_status_code, self._update_last_upload
        )

    def _update_last_upload(self, status_code: int) -> None:
        now = datetime.now().strftime("%x %X")
        if status_code is None:
            self._last_upload.SetLabel(f"Connection failed at {now}")
        elif status_code >= 200 and status_code < 300:
            self._last_upload.SetLabel(f"Upload succeeded at {now}.")
        else:
            self._last_upload.SetLabel(
                f"Upload failed with status code {status_code} at {now}."
            )
