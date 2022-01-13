import threading
from http.server import ThreadingHTTPServer

from huokanapiclient.client import Client
from rx.subject.subject import Subject

from huokanadvertiserclient.core.discord.OAuthHandler import (
    oauth_handler_with_return_url,
)


class OAuthServer:
    def __init__(self, port: int, api_client: Client, api_key_subject: Subject) -> None:
        self._server = ThreadingHTTPServer(
            ("localhost", port),
            oauth_handler_with_return_url(
                api_client,
                f"http://localhost:{port}",
                api_key_subject,
            ),
        )
        thread = threading.Thread(target=self._server.serve_forever)
        thread.setDaemon(True)
        thread.start()

    def destroy(self):
        self._server.shutdown()
