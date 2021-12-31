from rx.subject.subject import Subject
from huokan_client import Client
from huokanadvertiserclient.config.Configuration import Configuration
from huokanadvertiserclient.core.discord.OAuthServer import OAuthServer


class DiscordOAuthListener:
    def __init__(self, config: Configuration) -> None:
        client = Client(base_url=config.api_base_url, timeout=30, verify_ssl=True)
        self._port = 52602
        self._server = OAuthServer(self._port, client, config.api_key)

    def get_redirect_url(self) -> str:
        return f"http://localhost:{self._port}"

    def destroy(self) -> None:
        self._server.destroy()
