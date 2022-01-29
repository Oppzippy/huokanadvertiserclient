from datetime import datetime
from dateutil.relativedelta import relativedelta
from typing import Dict, List

from attr import dataclass


@dataclass
class DepositLogEntry:
    character_name: str
    character_realm: str
    guild_bank_copper: int
    deposit_in_copper: int
    approximate_deposit_timestamp: datetime


@dataclass
class DepositLog:
    log: List[DepositLogEntry]
    guild_name: str
    guild_realm: str
    captured_at: datetime


def parse_deposit_log_dict(raw_logs: List[Dict]) -> List[DepositLog]:
    return [_parse_deposit_log(log) for log in raw_logs]


def _parse_deposit_log(log: dict) -> DepositLog:
    captured_at = datetime.fromtimestamp(log["capturedAt"])
    return DepositLog(
        log=[
            DepositLogEntry(
                character_name=entry["characterName"],
                character_realm=entry["characterRealm"],
                guild_bank_copper=entry["guildBankCopper"],
                deposit_in_copper=entry["depositInCopper"],
                approximate_deposit_timestamp=_time_elapsed_to_datetime(
                    entry["timeElapsed"],
                    captured_at,
                ),
            )
            for entry in log["log"]
        ],
        guild_name=log["guildName"],
        guild_realm=log["guildRealm"],
        captured_at=captured_at,
    )


def _time_elapsed_to_datetime(time_elapsed: Dict, until: datetime) -> datetime:
    delta = relativedelta(
        years=time_elapsed["years"],
        months=time_elapsed["months"],
        days=time_elapsed["days"],
        hours=time_elapsed["hours"],
    )
    return until - delta
