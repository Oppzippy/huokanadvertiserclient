import wx
from pathlib import Path


class WoWDirPicker(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        sizer = wx.BoxSizer()

        self.wow_path_ctrl = wx.DirPickerCtrl(
            self, style=wx.DIRP_USE_TEXTCTRL | wx.DIRP_DIR_MUST_EXIST
        )
        sizer.Add(self.wow_path_ctrl)

        self.SetSizer(sizer)

    def set_path(self, path: str) -> None:
        self.wow_path_ctrl.SetPath(path)

    def get_path(self) -> str:
        return self.wow_path_ctrl.GetPath()

    def is_path_valid_wow_dir(self) -> bool:
        path = Path(self.get_path())
        if path.is_dir():
            return path.joinpath("Wow.exe").is_file()
        return False
