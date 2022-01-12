from typing import List, Union
from huokanadvertiserclient.core.depositlog.parser.DictToDataClass import (
    DepositLog,
    parse_deposit_log_dict,
)
from huokanadvertiserclient.core.depositlog.parser.LuaParser import (
    parse_deposit_logs_lua,
)


def parse_deposit_log(saved_variables: str) -> Union[List[DepositLog], None]:
    parsed_dict = parse_deposit_logs_lua(saved_variables)
    if parsed_dict is not None:
        return parse_deposit_log_dict(parsed_dict)
    return None
