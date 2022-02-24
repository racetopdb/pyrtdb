"""
    Constructor functions implementation conforming to pep248.
"""
import time
import datetime
from typing import Union


Date = datetime.date
Time = datetime.time
TimeDelta = datetime.timedelta
Timestamp = datetime
DateTimeDeltaType = datetime.timedelta
DateTimeType = datetime


def DateFromTicks(ticks):
    return datetime.date(*time.localtime(ticks)[:3])


def TimeFromTicks(ticks):
    return datetime.time(*time.localtime(ticks)[3:6])


def TimestampFromTicks(ticks):
    return datetime.datetime(*time.localtime(ticks)[:6])


def format_datetime(dt: datetime.datetime) -> str:
    """Converts an object of type datetime to a time string in the specified format.

    Args:
        dt (datetime.datetime): an object of type datetime
    """
    return dt.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]


def str2datetime(s: str) -> Union[datetime.datetime, datetime.date, None]:
    """Converts a string to an object of type datetime.

    Args:
        s (str): string
    """
    dt = None
    try:
        if len(s) < 11:
            return str2date(s)
        dt = datetime.datetime.strptime(s, "%Y-%m-%d %H:%M:%S.%f")
    except ValueError:
        pass
    return dt


def str2time(s: str) -> Union[time.struct_time, None]:
    """Converts a string to an object of type time.

    Args:
        s (str): string
    """
    t = None
    try:
        t = time.strptime(s, "%Y-%m-%d %H:%M:%S.%f")
    except ValueError:
        pass
    return t


def str2date(s: str) -> Union[datetime.date, None]:
    """Converts a string to an object of type date.

    Args:
        s (str): string
    """
    d = None
    try:
        d = datetime.datetime.strptime(s, "%Y-%m-%d").date()
    except ValueError:
        pass
    return d


def milli_timestamp2datetime(tp: int, is_local_time=True) -> Union[datetime.datetime, None]:
    dt = None
    try:
        if is_local_time:
            dt = datetime.datetime.utcfromtimestamp(
            tp / 1000) + datetime.timedelta(hours=8)
        else:
            dt = datetime.datetime.utcfromtimestamp(
                tp / 1000)
    except ValueError:
        pass
    return dt

