import re
from typing import Dict, List, Union

from slpp import slpp

from huokanadvertiserclient.core.depositlog.parser.DepositLogParserException import (
    DepositLogParserException,
)

_deposit_log_re = re.compile(
    "^HuokanAdvertiserToolsDepositLog = (\\{.*^\\})",
    re.MULTILINE | re.DOTALL,
)


def parse_deposit_logs_lua(content: str) -> Union[List[Dict], None]:
    deposit_log_match = _deposit_log_re.search(content)
    if deposit_log_match is not None:
        deposit_log_lua = deposit_log_match.group(1)
        deposit_log = slpp.decode(deposit_log_lua)
        if isinstance(deposit_log, list):
            return deposit_log
        else:
            raise DepositLogParserException(
                f"Expected deposit log to be a dict, got {type(deposit_log)}",
                deposit_log_lua,
            )
    return None
