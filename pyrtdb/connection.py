"""
This module implements the Connection class that supports PEP249.In most cases, you will generally use the default Cursor
class(with tuple rows).You can also specify to use DictCursor(with dict rows).
"""
import time

from .cursor import BaseCursor, Cursor
from .exception import *
from .constant import *
from .callso import RawTsdbClientV2

class Connection(RawTsdbClientV2):
    def __init__(self, host: str, port: int, user: str, password: str, **kwargs) -> None:
        """The rtdb connection

        Args:
            host (str): host to connect
            port (int): port of database server
            user (str): user
            password (str): password to connect

            /* arguments from kwargs, optional*/
            timeout(int): connection timeout
            charset(str): character set of database
            dbname (str): name of database
        """
        self._host = host if host else RTDB_HOST
        self._port = port if port else RTDB_PORT
        self._user = user if user else RTDB_USER_NAME
        self._password = password if password else RTDB_PASSWORD
        self.__db = None

        kwargs_copy = kwargs.copy()

        super().__init__(host, port, user, password, **kwargs)

        # default timeout = 30 seconds
        timeout = kwargs_copy.pop("timeout", 30)
        charset: str = kwargs_copy.pop("charset", None)
        dbname: str = kwargs_copy.pop("dbname", None)
        if charset and charset != self.charset:
            self.set_charset(charset)

        start_tm = time.time()
        self.connect()
        end_tm = time.time()

        if (end_tm - start_tm) > timeout:
            raise InterfaceError("connection timeout")

        if dbname:
            self.use_db(dbname)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def close(self):
        """Close database connection
        """
        self.disconnect()
        self.kill_tsdb()

    def commit(self):
        """Do not support dababase trasaction

        Raises:
            NotSupportedError
        """
        raise NotSupportedError

    def rollback(self):
        """Do not support dababase trasaction

        Raises:
            NotSupportedError
        """
        raise NotSupportedError

    def cursor(self, cursor_cls: BaseCursor = None):
        return cursor_cls(self) if cursor_cls else Cursor(self)

    def query(self, query: str):
        super().query(query)

    def set_charset(self, charset: str):
        charset_reverse = {v: k for k, v in CHARSET_DICT.items()}
        charset_id: int = charset_reverse.get(charset, None)
        if not charset_id:
            raise InvalidArgs(
                "invalid charset, input charset: {}".format(charset))

        super().set_charset(charset_id)
        self.charset = charset

    def use_db(self, dbname: str):
        if dbname:
            self.query("use {};".format(dbname))
            self.__db = dbname

    @property
    def db(self) -> str:
        """[summary]

        Returns:
            [str]: current database
        """
        return self.__db
