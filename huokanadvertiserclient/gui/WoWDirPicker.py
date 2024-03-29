from pathlib import Path

import wx
from rx.core.observable.observable import Observable
from rx.subject.subject import Subject

from huokanadvertiserclient.gui.framework.ReactivePanel import ReactivePanel


class WoWDirPicker(ReactivePanel):
    def __init__(self, parent, wow_path_subject: Subject):
        super().__init__(parent)
        self._path_subject = wow_path_subject

        sizer = wx.BoxSizer(wx.VERTICAL)
        self._dir_picker = wx.DirPickerCtrl(
            self, style=wx.DIRP_USE_TEXTCTRL | wx.DIRP_DIR_MUST_EXIST
        )
        sizer.Add(self._dir_picker, flag=wx.EXPAND)
        self._dir_picker.Bind(wx.EVT_DIRPICKER_CHANGED, self._on_change)
        self.SetSizer(sizer)

        self.bind_observable(wow_path_subject, self._dir_picker.SetPath)
        self.bind_observer(
            wow_path_subject,
            self._dir_picker,
            wx.EVT_DIRPICKER_CHANGED,
            get_new_value=self.get_path,
        )

    def set_path(self, path: str) -> None:
        self._on_change(path)

    def get_path(self) -> str:
        return self._dir_picker.GetPath()

    def get_path_observable(self) -> Observable:
        return self._path_subject

    def is_path_valid_wow_dir(self) -> bool:
        path = Path(self.get_path())
        if path.is_dir():
            return path.joinpath("Wow.exe").is_file()
        return False

    def _on_change(self, _: str) -> None:
        if self.is_path_valid_wow_dir():
            pass
        else:
            # TODO show some indocator of invalid dir
            pass
