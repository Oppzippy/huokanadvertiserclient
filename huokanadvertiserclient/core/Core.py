from huokanapiclient.client import AuthenticatedClient
from huokanadvertiserclient.state.State import State
from huokanadvertiserclient.core.depositlog.DepositLogWatcher import DepositLogWatcher


class Core:
    def __init__(self, state: State, api_client: AuthenticatedClient):
        self._deposit_log_watcher = DepositLogWatcher(state, api_client)

    def destroy(self):
        self._deposit_log_watcher.destroy()
