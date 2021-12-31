import threading
from http.server import ThreadingHTTPServer
from huokanadvertiserclient.core.discord.OAuthHandler import (
    oauth_handler_with_return_url,
)


class OAuthServer:
    def __init__(self, port: int) -> None:
        self._server = ThreadingHTTPServer(
            ("127.0.0.1", port),
            oauth_handler_with_return_url(f"http://127.0.0.1:{port}"),
        )
        thread = threading.Thread(target=self._server.serve_forever)
        thread.setDaemon(True)
        thread.start()

    def destroy(self):
        self._server.shutdown()
