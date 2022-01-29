import logging
from os import environ
from pathlib import Path

import sentry_sdk
from sentry_sdk.integrations.httpx import HttpxIntegration

from __init__ import __version__
from huokanadvertiserclient.GUIApplication import GUIApplication
from huokanadvertiserclient.state.State import State

sentry_sdk.init(
    "https://63ba5c7a6179488f9d0e00ad45d1037d@o507151.ingest.sentry.io/6173667",
    traces_sample_rate=0.0025,
    release=f"huokanclient@{__version__}",
    max_breadcrumbs=25,
    with_locals=True,
    request_bodies="small",
    integrations=[HttpxIntegration()],
)


def get_config_dir() -> Path:
    if "APPDATA" in environ:
        return Path(environ["APPDATA"])
    elif "XDG_CONFIG_HOME" in environ:
        return Path(environ["XDG_CONFIG_HOME"])
    else:
        return Path(environ["HOME"]).joinpath(".config")


state = State(get_config_dir().joinpath("huokanclient", "config.json").__str__())
logging.basicConfig(
    format="%(asctime)s %(threadName)s [%(levelname)s]  %(message)s",
    encoding="utf-8",
    level=logging.INFO,
    handlers=[
        logging.FileHandler(
            get_config_dir().joinpath("huokanclient", "log.txt"), "w", "utf-8"
        ),
        logging.StreamHandler(),
    ],
)

app = GUIApplication(state)
app.main_loop()
