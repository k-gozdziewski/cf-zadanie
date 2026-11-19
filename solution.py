import operator
import re
import pandas as pd

RULE_PATTERN = re.compile(r"\s*(\w+)\s*([+\-*])\s*(\w+)\s*")
COLUMN_NAME_PATTERN = re.compile(r"[A-Za-z]+(?:_[A-Za-z]+)*")
OPERATIONS = {"+": operator.add, "-": operator.sub, "*": operator.mul}


def add_virtual_column(df: pd.DataFrame, role: str, new_column: str) -> pd.DataFrame:
    empty = pd.DataFrame([])

    if not isinstance(new_column, str) or not COLUMN_NAME_PATTERN.fullmatch(new_column):
        return empty

    rule_match = RULE_PATTERN.fullmatch(role)
    if not rule_match:
        return empty
    left, op, right = rule_match.groups()

    if left not in df.columns or right not in df.columns:
        return empty

    result_values = OPERATIONS[op](df[left],df[right])

    result = df.copy()
    result[new_column] = result_values
    return result