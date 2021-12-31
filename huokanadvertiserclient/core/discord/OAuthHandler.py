from http.server import BaseHTTPRequestHandler
import socketserver


def oauth_handler_with_return_url(return_url: str):
    class OAuthHandler(BaseHTTPRequestHandler):
        def __init__(
            self,
            request: bytes,
            client_address: tuple[str, int],
            server: socketserver.BaseServer,
        ) -> None:
            super().__init__(request, client_address, server)

        def do_GET(self) -> None:
            print(self.path, return_url)

    return OAuthHandler
