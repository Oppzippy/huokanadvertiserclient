import logging
from os import environ
from pathlib import Path
from typing import Union

import sentry_sdk
import wx
from huokanapiclient.api.users import get_me
from huokanapiclient.client import AuthenticatedClient
from sentry_sdk.integrations.httpx import HttpxIntegration

from __init__ import __version__
from huokanadvertiserclient.core.Core import Core
from huokanadvertiserclient.gui.RootFrame import RootFrame
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


config = State(get_config_dir().joinpath("huokanclient", "config.json").__str__())
logging.basicConfig(
    filename=get_config_dir().joinpath("huokanclient", "log.txt"),
    format="%(asctime)s %(threadName)s [%(levelname)s]  %(message)s",
    encoding="utf-8",
    level=logging.DEBUG,
)


core: Union[Core, None] = None


def on_api_key_update(api_key: str):
    global core
    if core is not None:
        logging.debug("API key changed, destroying Core")
        core.destroy()
        core = None
        sentry_sdk.set_user(None)

    if api_key is not None:
        logging.debug("API key is set, creating Core")
        authenticated_client = AuthenticatedClient(
            config.api_base_url.value,
            api_key,
            headers={"User-Agent": f"huokanapiclient v{__version__}"},
            timeout=10,
            verify_ssl=True,
        )
        me = get_me.sync_detailed(client=authenticated_client)
        if me.status_code >= 200 and me.status_code < 300 and me.parsed is not None:
            sentry_sdk.set_user(
                {"id": me.parsed.id, "discordUserId": me.parsed.discord_user_id}
            )
            core = Core(
                config,
                authenticated_client,
            )
        else:
            logging.info(
                "Failed to authenticate with api key, got status code %d when retrieving user info",
                me.status_code,
            )


config.api_key.subscribe(on_next=on_api_key_update)


app = wx.App()

frame = RootFrame(config)
frame.Show()

app.MainLoop()
