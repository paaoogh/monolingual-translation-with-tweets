"""Decorators for sanity checks."""

import functools
from dataclasses import dataclass
from pandas import DataFrame
import pandas as pd


@dataclass
class MessageError:
    """Messages for error rising."""

    missing_name_column: str = (
        "Dataframe must have name column. Check accepted format on documentation."
    )
    missing_user_column: str = (
        "Dataframe must have user column. Check accepted format on documentation."
    )
    empty_data_frame: str = "No registries found at file"
    not_strings: str = "All elements in the dataframe must be strings"
    date_formats: str = (
        "Date is not with accepted format. Check accepted format on documentation."
    )


def check_dataframe_integrity(func):
    """Basic sanity checks for dataframe

    Raises:
        ValueError: Not valid name columns
        ValueError: Not valid date columns
        ValueError: Not valid datatype for name columns
        ValueError: Empty dataframes
        ValueError: No date at columns
    """
    errors = MessageError()
    accepted_user_columns = ["Usuario", "usuario", "User", "user"]
    accepted_name_columns = ["Name", "name", "nombre", "nombre"]
    accepted_start_date_columns = [
        "Fecha de inicio",
        "fecha de inicio",
        "start date",
        "Start date",
    ]

    @functools.wraps(func)
    def wrapper_users(df: DataFrame, *args, **kwargs):
        if not all(col in df.columns for col in accepted_name_columns):
            raise ValueError(errors.missing_name_column)
        if not all(col in df.columns for col in accepted_user_columns):
            raise ValueError(errors.missing_user_column)
        if not all(pd.api.types.is_string_dtype(col) for col in df.dtypes):
            raise ValueError(errors.not_strings)
        if not all(col in df.columns for col in accepted_start_date_columns):
            raise ValueError(errors.missing_user_column)
        if df.empty:
            raise ValueError(errors.empty_data_frame)
        return func(df, *args, **kwargs)

    return wrapper_users


def check_date_integrity_dataframe(func):
    """Checks date column can be converted to date dataype"""

    @functools.wraps(func)
    def wrapper_date_format(df: DataFrame, date_column: str, *args, **kwargs):
        try:
            pd.to_datetime(df[date_column])
        except Exception:
            raise ValueError("Incorrecy date format.")
        return func(df, *args, **kwargs)

    return wrapper_date_format
