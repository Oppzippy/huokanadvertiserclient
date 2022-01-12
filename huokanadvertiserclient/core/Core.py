from huokanapiclient.client import AuthenticatedClient
from huokanadvertiserclient.config.Configuration import Configuration
from huokanadvertiserclient.core.depositlog.DepositLogWatcher import DepositLogWatcher


class Core:
    def __init__(self, config: Configuration, api_client: AuthenticatedClient):
        self._deposit_log_watcher = DepositLogWatcher(config, api_client)

    def destroy(self):
        self._deposit_log_watcher.destroy()
