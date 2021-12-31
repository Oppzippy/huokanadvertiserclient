import re
from http.server import BaseHTTPRequestHandler
from typing import Tuple
from huokan_client import Client
from huokan_client.api.discord_authorization import authorize
from rx.subject.subject import Subject
import socketserver


def oauth_handler_with_return_url(
    api_client: Client,
    return_url: str,
    api_key_subject: Subject,
):
    class OAuthHandler(BaseHTTPRequestHandler):
        def __init__(
            self,
            request: bytes,
            client_address: Tuple[str, int],
            server: socketserver.BaseServer,
        ) -> None:
            super().__init__(request, client_address, server)

        def do_GET(self) -> None:
            code = re.findall("[\\?&]code=([^\\?&]+)", self.path)
            if len(code) >= 1:
                auth = authorize.sync(
                    client=api_client,
                    code=code[0],
                    redirect_url=return_url,
                )
                api_key_subject.on_next(auth.api_key if auth is not None else None)

    return OAuthHandler
