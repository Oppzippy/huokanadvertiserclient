import wx

from huokanadvertiserclient.core.Core import Core
from huokanadvertiserclient.gui.RootFrame import RootFrame
from huokanadvertiserclient.state.State import State


class GUIApplication:
    def __init__(self, state: State):
        self._state = state
        self._core = Core(self._state)

        self._app = wx.App()
        self._root_frame = RootFrame(self._state)
        self._root_frame.Show()

    def main_loop(self) -> None:
        self._app.MainLoop()
