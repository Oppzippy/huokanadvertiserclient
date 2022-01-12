from huokanapiclient.models.deposit_log_entry import DepositLogEntry
from huokanadvertiserclient.core.depositlog.parser.DictToDataClass import DepositLog
from huokanapiclient.models.deposit_log import DepositLog as ApiDepositLog


def to_api_deposit_log(deposit_log: DepositLog) -> ApiDepositLog:
    return ApiDepositLog(
        log=[
            DepositLogEntry(
                entry.character_name,
                entry.character_realm,
                entry.deposit_in_copper,
                entry.guild_bank_copper,
            )
            for entry in deposit_log.log
        ],
        captured_at=deposit_log.captured_at,
    )
