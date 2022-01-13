from huokanapiclient.client import Client

from huokanadvertiserclient.core.discord.OAuthServer import OAuthServer
from huokanadvertiserclient.state.State import State


class OAuthListener:
    def __init__(self, state: State) -> None:
        client = Client(base_url=state.api_base_url.value, timeout=30, verify_ssl=True)
        self._port = 52602
        self._server = OAuthServer(self._port, client, state.api_key)

    def get_redirect_url(self) -> str:
        return f"http://localhost:{self._port}"

    def destroy(self) -> None:
        self._server.destroy()
