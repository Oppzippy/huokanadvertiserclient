import logging
from pathlib import Path

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
    def __init__(self, state: State, api_client: AuthenticatedClient) -> None:
        self._api_client = api_client
        self._state = state
        self._subject = Subject()
        self._watcher = SavedVariablesWatcher(state.wow_path, self._subject)
        self._subject.subscribe(on_next=self.upload_log_from_file)

    def upload_log_from_file(self, file_path: Path):
        content = file_path.read_text()
        deposit_logs = parse_deposit_log(content)
        if deposit_logs is None:
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
        except:
            self._state.deposit_log_upload_status_code.on_next(None)

    def destroy(self) -> None:
        self._watcher.destroy()
        self._subject.dispose()
