from os import environ
import wx
from huokanadvertiserclient.gui.RootFrame import RootFrame
from huokanadvertiserclient.config.Configuration import Configuration
from pathlib import Path

config_dir: Path
if "APPDATA" in environ:
    config_dir = Path(environ["APPDATA"])
elif "XDG_CONFIG_HOME" in environ:
    config_dir = Path(environ["XDG_CONFIG_HOME"])
else:
    config_dir = Path(environ["HOME"]).joinpath(".config")

config = Configuration(config_dir.joinpath("huokanclient", "config.json").__str__())
config.save()

app = wx.App()

frame = RootFrame(config)
frame.Show()

app.MainLoop()
