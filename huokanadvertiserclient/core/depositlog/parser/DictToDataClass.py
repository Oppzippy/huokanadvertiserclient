from typing import Dict, List
from attr import dataclass
from datetime import datetime


@dataclass
class DepositLogEntry:
    character_name: str
    character_realm: str
    guild_bank_copper: int
    deposit_in_copper: int


@dataclass
class DepositLog:
    log: List[DepositLogEntry]
    guild_name: str
    guild_realm: str
    captured_at: datetime


def parse_deposit_log_dict(raw_logs: List[Dict]) -> List[DepositLog]:
    return [
        DepositLog(
            log=[
                DepositLogEntry(
                    character_name=entry["characterName"],
                    character_realm=entry["characterRealm"],
                    guild_bank_copper=entry["guildBankCopper"],
                    deposit_in_copper=entry["depositInCopper"],
                )
                for entry in log["log"]
            ],
            guild_name=log["guildName"],
            guild_realm=log["guildRealm"],
            captured_at=datetime.fromtimestamp(log["capturedAt"]),
        )
        for log in raw_logs
    ]
