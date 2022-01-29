from typing import Union

from huokanapiclient.client import AuthenticatedClient

from huokanadvertiserclient.core.depositlog.DepositLogWatcher import DepositLogWatcher
from huokanadvertiserclient.core.login.LoginHandler import LoginHandler
from huokanadvertiserclient.state.State import State


class Core:
    def __init__(self, state: State):
        self._state = state
        self._login_handler: Union[LoginHandler, None] = None
        self._deposit_log_watcher: Union[DepositLogWatcher, None] = None

        self._state.api_key.subscribe(on_next=self.log_in)
        self._state.api_client.subscribe(on_next=self._on_login)

    def log_in(self, api_key: Union[str, None]) -> None:
        if self._login_handler is not None:
            self._login_handler.cancel()
        if api_key is None:
            self._state.api_client.on_next(None)
            return

        client = AuthenticatedClient(
            self._state.api_base_url.value,
            api_key,
            headers={"User-Agent": f"huokanapiclient"},
            timeout=10,
            verify_ssl=True,
        )
        self._login_handler = LoginHandler(client)
        observable = self._login_handler.log_in()
        observable.subscribe(
            on_completed=lambda: self._state.api_client.on_next(client),
        )

    def cancel_login(self):
        if self._login_handler is not None:
            self._login_handler.cancel()
            self._login_handler = None

    def _on_login(self, client: Union[AuthenticatedClient, None]) -> None:
        self.log_out()

        if client is not None:
            self._deposit_log_watcher = DepositLogWatcher(self._state)

    def destroy(self):
        self.log_out()

    def log_out(self):
        if self._deposit_log_watcher is not None:
            self._deposit_log_watcher.destroy()
            self._deposit_log_watcher = None
