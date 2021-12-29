import wx
from pathlib import Path
from rx.core.observable.observable import Observable
from rx.subject.behaviorsubject import BehaviorSubject


class WoWDirPicker(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)

        self._path = BehaviorSubject(None)

        sizer = wx.BoxSizer(wx.VERTICAL)
        self._dir_picker = wx.DirPickerCtrl(
            self, style=wx.DIRP_USE_TEXTCTRL | wx.DIRP_DIR_MUST_EXIST
        )
        sizer.Add(self._dir_picker, flag=wx.EXPAND)
        self.SetSizer(sizer)

        self._dir_picker.Bind(wx.EVT_DIRPICKER_CHANGED, self._on_change)

    def set_path(self, path: str) -> None:
        self._dir_picker.SetPath(path or "")
        self._on_change(path)

    def get_path(self) -> str:
        return self._dir_picker.GetPath()

    def get_path_observable(self) -> Observable:
        return self._path

    def is_path_valid_wow_dir(self) -> bool:
        path = Path(self.get_path())
        if path.is_dir():
            return path.joinpath("Wow.exe").is_file()
        return False

    def _on_change(self, path: str) -> None:
        if self.is_path_valid_wow_dir():
            self._path.on_next(self.get_path())
        else:
            self._path.on_next(None)
            # TODO show some indocator of invalid dir
            pass
