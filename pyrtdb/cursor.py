"""
This module implements Cursors of race time db.It contains the default Cursor class、optional DictCursor class and the base Cursor class.
"""
import re
from typing import Iterable, Tuple, Union, Dict
from functools import wraps

from .log import rtdb_logger_singleton
from .exception import DataError, ProgrammingError
from .converter import Converter
from .constant import DEBUG_PRINT_SQL

INSERT_VALUES_PATTERN = re.compile(
    "".join(
        [
            r"\s*((?:INSERT|REPLACE)\b.+\bVALUES?\s*)",
            r"(\(\s*(?:%s|%\(.+\)s)\s*(?:,\s*(?:%s|%\(.+\)s)\s*)*\))",
        ]
    ),
    re.IGNORECASE | re.DOTALL,
)


def must_be_executed(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        self: BaseCursor = args[0]
        if not self._executed:
            raise ProgrammingError("must be executed first")
        if not self._rows or self.rownumber >= len(self._rows):
            return None

        return func(*args, **kwargs)

    return wrapper


class BaseCursor:
    def __init__(self, connection) -> None:
        self.connection = connection
        self._rowcount = -1
        self.arraysize = 1
        self._executed = None
        self._result = None
        self._rows: Union[Iterable, None] = None
        self._encoder = Converter()
        self.rownumber = 0

    @property
    def rowcount(self) -> int:
        return self._rowcount

    def close(self):
        if not self.connection:
            return

        self.connection = None
        self._result = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def execute(self, query: str, args: Union[Tuple, Dict] = None):
        query_fmt = query
        if args:
            if query.count("%s") != len(args):
                raise ProgrammingError("number of parameters does not match")
            
            query_fmt = query.replace("%s", "{}")
            if isinstance(args, Tuple):
                # query_fmt = query_fmt.format(*args)
                query_fmt = query_fmt.format(*(self._encoder.convert(arg) for arg in args))
            elif isinstance(args, Dict):
                query_fmt = query_fmt.format(**args)
            else:
                raise DataError("the parameter type must be tuple or dict")
        if DEBUG_PRINT_SQL:
            rtdb_logger_singleton().debug(query_fmt)
        return self._query(query_fmt)

    def _query(self, query: str):
        db = self._get_db()
        self._reset_result()
        db.query(query)
        db.store_result()
        self._read_result(db)
        self._clean_result()
        self._executed = query
        return self.rowcount

    def executemany(self):
        pass
    
    def _reset_result(self):
        self._result = None
        self._rowcount = -1
        self.rownumber = 0
        self._rows = None

    @must_be_executed
    def fetchone(self):
        result = self._rows[self.rownumber]
        self.rownumber += 1
        return result

    @must_be_executed
    def fetchmany(self, size=None):
        end = self.rownumber + (size or self.arraysize)
        result = self._rows[self.rownumber: end]
        self.rownumber = min(end, len(self._rows))
        return result

    @must_be_executed
    def fetchall(self):
        result = self._rows[self.rownumber:] if self.rownumber else self._rows
        self.rownumber = len(self._rows)
        return result

    def _get_db(self):
        """

        Raises:
            ProgrammingError: cursor closed

        Returns:
            [Connection]: database connection
        """
        if not self.connection:
            raise ProgrammingError("cursor closed")

        return self.connection

    def _read_result(self, db):
        """

        Args:
            db (Connection): database connection
        """
        # TODO 实现describe函数描述元信息
        if not db.result:
            return
        self._result = db.result
        self._rowcount = db.affected_rows()
        self.rownumber = 0
        self._rows = db.fetch_rows(self._rows_type)

    def _clean_result(self):
        if self._result:
            db = self._get_db()
            self._result = None
            db.free_result()

    def __iter__(self):
        return iter(self._rows[self.rownumber:] if self.rownumber else self._rows)

    def __next__(self):
        row = self.fetchone()
        if not row:
            raise StopIteration
        return row


class TupleRowsCursor:
    _rows_type = 0


class DictRowsCursor:
    _rows_type = 1


class Cursor(BaseCursor, TupleRowsCursor):
    pass


class DictCursor(BaseCursor, DictRowsCursor):
    pass
