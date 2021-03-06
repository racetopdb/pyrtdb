from .time import (
    Date,
    Time,
    TimeDelta,
    Timestamp,
    DateTimeDeltaType,
    DateTimeType,
    DateFromTicks,
    TimeFromTicks,
    TimestampFromTicks
)
# from .datastructure import DataType
from .constant import (
    CHARSET_UNKNOWN,
    CHARSET_GBK,
    CHARSET_UTF8,
    CHARSET_UCS2LE,
    CHARSET_UCS2BE,
    CHARSET_BIG5,
    CHARSET_EUCJP,
    CHARSET_SJIS,
    CHARSET_EUCKR,
    CHARSET_ISO1,
    CHARSET_WIN1,
    CHARSET_WIN2,

    CharsetID,

    RTDB_USER_NAME,
    RTDB_HOST,
    RTDB_PASSWORD,
    RTDB_PORT
)
from .exception import (
    InterfaceError,
    DatabaseError,
    InternalError,
    OperationalError,
    ProgrammingError,
    IntegrityError,
    DataError,
    NotSupportedError,
    InvalidArgs
)

from .rtdb_pool import rtdb_pool

threadsafety = 1
apilevel = "2.0"
paramstyle = "format"

def NewPool(host: str, port: int, user: str, password: str,**kwargs):
    return rtdb_pool(host,port,user,password,**kwargs)

class TypeSet(frozenset):
    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, TypeSet):
            return not self.difference(__o)
        return __o in self


# Binary = TypeSet([DataType.Binary.value])
# STRING = TypeSet([DataType.String.value])
# NUMBER = TypeSet([DataType.Int.value, DataType.Int64.value,
#                 DataType.Float.value, DataType.Double.value])
# DATETIME = TypeSet([DataType.Timestamp.value])
# ROWID = TypeSet([DataType.Int64.value])


__all__ = [
    "Date",
    "Time",
    "TimeDelta",
    "Timestamp",
    "DateTimeDeltaType",
    "DateTimeType",
    "DateFromTicks",
    "TimeFromTicks",
    "TimestampFromTicks",

    "InterfaceError",
    "DatabaseError",
    "InternalError",
    "OperationalError",
    "ProgrammingError",
    "IntegrityError",
    "DataError",
    "NotSupportedError",
    "InvalidArgs",

    "RTDB_USER_NAME",
    "RTDB_HOST",
    "RTDB_PASSWORD",
    "RTDB_PORT"
]
