from ctypes import c_void_p
from typing import Union, Tuple, Dict

from . import rtdb_pool, ProgrammingError, DataError
from .adaptor.rtdb_v3 import rtdb_v3
from .constant import DEBUG_PRINT_SQL
from .log import rlogger
from .rtdb_reader import rtdb_reader


class rtdb(rtdb_v3):
    def __init__(self,pool: rtdb_pool,c_tsdb:c_void_p,conn_url:str):
        rtdb_v3.__init__(self,pool,c_tsdb)
        self._conn_url = conn_url

    def newConn(self)->"rtdb":
       r = self.connect(self._conn_url)
       if 0 == r :
           return self
       return None

    def query_reader(self, sql: str, charset: str = "", database: str = "",fetch_first_line:bool = False) -> rtdb_reader:
        c_reader = rtdb_v3.query_reader(self,sql,charset,database,fetch_first_line)
        if not c_reader:
            return None
        return rtdb_reader(self.pool(), c_reader)

    def query(self, sql: str, charset: str = "", database: str = "") -> int:
        return rtdb_v3.query(self,sql,charset,database);

    def query_result(self) -> rtdb_reader:
        c_reader = rtdb_v3.store_result(self)
        if not c_reader:
            return None
        return rtdb_reader(self.pool(), c_reader)

    def print_stdout(self) -> int:
        return rtdb_v3.print_stdout(self, "")

    def print_str(self) -> str:
        return rtdb_v3.print_str(self, "")
