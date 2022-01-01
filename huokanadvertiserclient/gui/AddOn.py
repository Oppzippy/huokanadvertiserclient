from pathlib import Path
import wx
import re
from typing import Union

from rx.core.observable.observable import Observable

from huokanadvertiserclient.gui.framework.ReactivePanel import ReactivePanel


class AddOn(ReactivePanel):
    def __init__(self, parent, wow_path: Observable):
        super().__init__(parent)

        sizer = wx.BoxSizer(wx.VERTICAL)
        self._current_version = wx.StaticText(self)

        sizer.Add(self._current_version, flag=wx.EXPAND)
        self.SetSizer(sizer)
        self.bind_observable(wow_path, self._update_version_text)

    def _update_version_text(self, wow_path: Union[str, None]) -> None:
        if wow_path is None:
            self._current_version.SetLabel("Unknown")
            return
        path = Path(wow_path)
        toc_path = path.joinpath(
            "Interface", "AddOns", "HuokanAdvertiserTools", "HuokanAdvertiserTools.toc"
        )
        if not toc_path.is_file():
            self._current_version.SetLabel("Not Installed")
            return

        toc = toc_path.read_text()
        matches = re.findall("^## Version: (.*)$", toc, re.MULTILINE)
        version = matches[-1] if len(matches) > 0 else "Corrupted Install"
        self._current_version.SetLabel(f"Installed Version: {version}")
