from os import environ
from pathlib import Path
from typing import Union

import wx
from huokanapiclient.client import AuthenticatedClient

from huokanadvertiserclient.core.Core import Core
from huokanadvertiserclient.gui.RootFrame import RootFrame
from huokanadvertiserclient.state.State import State

config_dir: Path
if "APPDATA" in environ:
    config_dir = Path(environ["APPDATA"])
elif "XDG_CONFIG_HOME" in environ:
    config_dir = Path(environ["XDG_CONFIG_HOME"])
else:
    config_dir = Path(environ["HOME"]).joinpath(".config")

config = State(config_dir.joinpath("huokanclient", "config.json").__str__())

core: Union[Core, None] = None


def on_api_key_update(api_key: str):
    global core
    if core is not None:
        core.destroy()
        core = None

    if api_key is not None:
        core = Core(
            config,
            AuthenticatedClient(
                config.api_base_url.value,
                api_key,
                headers={"User-Agent": "huokanapiclient"},
                timeout=10,
                verify_ssl=True,
            ),
        )


config.api_key.subscribe(on_next=on_api_key_update)


app = wx.App()

frame = RootFrame(config)
frame.Show()

app.MainLoop()
