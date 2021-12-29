import wx
from rx.core.observable.observable import Observable

from huokanclient.gui.WoWDirPicker import WoWDirPicker
from huokanclient.config.Configuration import Configuration


class Settings(wx.Panel):
    def __init__(self, parent, config: Configuration):
        super().__init__(parent)
        self._config = config

        sizer = wx.BoxSizer(wx.VERTICAL)
        self._dir_picker = WoWDirPicker(self)
        self._dir_picker.set_path(config.get_wow_path())
        self.get_wow_path_observable().subscribe(on_next=self.update_wow_path_in_config)

        sizer.Add(self._dir_picker, flag=wx.EXPAND)
        self.SetSizer(sizer)

    def update_wow_path_in_config(self, new_path: str):
        self._config.set_wow_path(new_path)
        self._config.save()

    def get_wow_path_observable(self) -> Observable:
        return self._dir_picker.get_path_observable()
