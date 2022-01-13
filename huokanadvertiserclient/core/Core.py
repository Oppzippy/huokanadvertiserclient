from huokanapiclient.client import AuthenticatedClient

from huokanadvertiserclient.core.depositlog.DepositLogWatcher import DepositLogWatcher
from huokanadvertiserclient.state.State import State


class Core:
    def __init__(self, state: State, api_client: AuthenticatedClient):
        self._deposit_log_watcher = DepositLogWatcher(state, api_client)

    def destroy(self):
        self._deposit_log_watcher.destroy()
