import logging
from pathlib import Path
from threading import Lock, Thread
from typing import Union
import httpx

from huokanapiclient.api.deposit_logs import import_deposit_log
from huokanapiclient.api.guilds import get_guilds
from huokanapiclient.client import AuthenticatedClient
from rx.subject.subject import Subject

from huokanadvertiserclient.core.apiutil.GetGuildId import to_api_deposit_log
from huokanadvertiserclient.core.depositlog.parser.Parser import parse_deposit_log
from huokanadvertiserclient.core.depositlog.SavedVariablesWatcher import (
    SavedVariablesWatcher,
)
from huokanadvertiserclient.state.State import State


class DepositLogWatcher:
    def __init__(self, state: State) -> None:
        self._state = state
        self._lock = Lock()
        self._subject = Subject()
        self._is_destroyed = False
        self._api_client: Union[AuthenticatedClient, None] = None

        self._unsubscribe = self._state.api_client.subscribe(
            on_next=self._set_api_client
        )

        self.upload_all_logs()

        self._watcher = SavedVariablesWatcher(state.wow_path, self._subject)
        self._subject.subscribe(on_next=self.upload_log_from_file)

    def _set_api_client(self, api_client: Union[AuthenticatedClient, None]) -> None:
        if api_client is not None and not self._is_destroyed:
            self._api_client = api_client

    def upload_all_logs(self):
        path = Path(self._state.wow_path.value)
        for file in path.glob("WTF/Account/*/SavedVariables/HuokanAdvertiserTools.lua"):
            thread = Thread(target=self.upload_log_from_file, args=(file,))
            thread.start()

    def upload_log_from_file(self, file_path: Path):
        content = file_path.read_text()
        deposit_logs = parse_deposit_log(content)
        if deposit_logs is None:
            return
        # Don't allow multiple calls of this function to send HTTP requests to the server at the same time
        # to ensure the server won't ever get spammed with requests.
        with self._lock:
            if self._is_destroyed or self._api_client is None:
                return
            try:
                for log in deposit_logs:
                    guilds = get_guilds.sync_detailed(
                        self._state.organization_id.value,
                        client=self._api_client,
                        name=log.guild_name,
                        realm=log.guild_realm,
                    )
                    if guilds.parsed:
                        guild = guilds.parsed.guilds[0]
                        upload_response = import_deposit_log.sync_detailed(
                            self._state.organization_id.value,
                            guild.id,
                            client=self._api_client,
                            json_body=to_api_deposit_log(log),
                        )
                        self._state.deposit_log_upload_status_code.on_next(
                            upload_response.status_code
                        )
                    else:
                        logging.info("failed to parse response")
                        self._state.deposit_log_upload_status_code.on_next(None)
            except httpx.RequestError:
                self._state.deposit_log_upload_status_code.on_next(None)
                logging.exception("Error uploading logs")

    def destroy(self) -> None:
        self._watcher.destroy()
        self._subject.dispose()
        self._unsubscribe.dispose()
        self._is_destroyed = True
