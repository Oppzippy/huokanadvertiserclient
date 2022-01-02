import re
from http.server import BaseHTTPRequestHandler
from typing import Callable, Tuple
from huokan_client import Client
from huokan_client.api.discord_authorization import authorize
from rx.subject.subject import Subject
import socketserver


class OAuthHandler(BaseHTTPRequestHandler):
    def __init__(
        self,
        request: bytes,
        client_address: Tuple[str, int],
        server: socketserver.BaseServer,
        api_client: Client,
        return_url: str,
        api_key_subject: Subject,
    ) -> None:
        self._api_client = api_client
        self._return_url = return_url
        self._api_key_subject = api_key_subject
        super().__init__(request, client_address, server)

    def do_GET(self) -> None:
        code = re.findall("[\\?&]code=([^\\?&]+)", self.path)
        if len(code) >= 1:
            response = authorize.sync_detailed(
                client=self._api_client,
                code=code[0],
                redirect_url=self._return_url,
            )
            if response.parsed is not None:
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b"Logged in. You can close this tab.")
            else:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(b"Login failed.")

            self._api_key_subject.on_next(
                response.parsed.api_key if response.parsed is not None else None
            )
        else:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"Code not specified")


def oauth_handler_with_return_url(
    api_client: Client,
    return_url: str,
    api_key_subject: Subject,
) -> Callable[[bytes, Tuple[str, int], socketserver.BaseServer], OAuthHandler]:
    def create(
        request: bytes,
        client_address: Tuple[str, int],
        server: socketserver.BaseServer,
    ) -> OAuthHandler:
        handler = OAuthHandler(
            request,
            client_address,
            server,
            api_client=api_client,
            return_url=return_url,
            api_key_subject=api_key_subject,
        )
        handler._api_client = api_client
        handler._return_url = return_url
        handler._api_key_subject = api_key_subject
        return handler

    return create
