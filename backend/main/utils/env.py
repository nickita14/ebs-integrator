import os
from typing import Iterable


class EnvironmentException(Exception):
    pass


class MissingEnvironmentValueException(EnvironmentException):
    pass


class ParsingEnvironmentValueException(EnvironmentException):
    pass


class DefaultEnvironmentValueException(EnvironmentException):
    pass


def get_bool(key: str, default: bool = None) -> bool:
    try:
        value = os.environ[key]
    except KeyError as e:
        if default is None:
            raise MissingEnvironmentValueException() from e
        if not isinstance(default, bool):
            raise DefaultEnvironmentValueException() from e
        return default
    else:
        if isinstance(value, str):
            upper_value = value.upper()
            if upper_value in ('', '0', 'N', 'NO', 'FALSE'):
                return False
            elif upper_value in ('1', 'Y', 'YES', 'TRUE'):
                return True
            raise ParsingEnvironmentValueException()

        try:
            return bool(value)
        except TypeError as e:
            raise ParsingEnvironmentValueException() from e


def get_list(key: str, default: Iterable[str] = None, separator: str = ' ') -> Iterable[str]:
    try:
        value = os.environ[key]
    except KeyError as e:
        if default is None:
            raise MissingEnvironmentValueException() from e
        if not isinstance(default, Iterable):
            raise DefaultEnvironmentValueException() from e
        return default
    else:
        return value.split(separator)


def get_int(key: str, default: int = None) -> int:
    try:
        value = os.environ[key]
    except KeyError as e:
        if default is None:
            raise MissingEnvironmentValueException() from e
        if not isinstance(default, int):
            raise DefaultEnvironmentValueException() from e
        return default
    else:
        try:
            return int(value)
        except ValueError as e:
            raise ParsingEnvironmentValueException() from e


def get_str(key: str, default: str = None) -> str:
    try:
        value = os.environ[key]
    except KeyError as e:
        if default is None:
            raise MissingEnvironmentValueException() from e
        if not isinstance(default, str):
            raise DefaultEnvironmentValueException() from e
        return default
    else:
        return value
