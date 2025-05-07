import re
from sqlalchemy import func

def normalize_column(column):
    return func.replace(
        func.replace(
            func.replace(
                func.replace(func.lower(func.trim(column)), ".", ""),
                "-", ""
            ),
            "'", ""
        ),
        " ", ""
    )

def normalize_search_text(text: str) -> str:
    return re.sub(r"[.\-'\s]", "", text.strip().lower())

def abs_column(column):
    return func.abs(column)