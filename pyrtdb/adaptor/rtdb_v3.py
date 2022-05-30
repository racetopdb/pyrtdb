import ctypes
from ctypes import  c_void_p

from pyrtdb.adaptor import rtdb_pool_v3
from pyrtdb.adaptor.so import str2c_char_p


class rtdb_v3:
    def __init__(self, pool: rtdb_pool_v3,c_tsdb:c_void_p):
        self._pool = pool
        self._c_tsdb = c_tsdb

    def _libdll(self):
        return self._pool.libdll()

    def pool(self):
        return self._pool

    
    def connect(self,conn_str: str) -> int:
        func = self._libdll().tsdb_v3_connect_private
        func.argtypes = (ctypes.c_void_p,ctypes.c_char_p,)
        func.restype = ctypes.c_int
        return func(self._c_tsdb,str2c_char_p(conn_str))

    
    def disconnect(self) -> int:
        func = self._libdll().tsdb_v3_disconnect
        func.argtypes = (ctypes.c_void_p,)
        func.restype = ctypes.c_int
        return func(self._c_tsdb)

    
    def get_user_name(self) -> str:
        tsdb_user_name = self._libdll.tsdb_v3_get_user_name
        tsdb_user_name.argtypes = (ctypes.c_void_p,)
        tsdb_user_name.restype = ctypes.c_char_p

        result: bytes = tsdb_user_name(self._tsdb)
        return result.decode(encoding='utf-8')

    
    def get_server_addr(self) -> str:
        tsdb_user_name = self._libdll.tsdb_v3_get_server_addr
        tsdb_user_name.argtypes = (ctypes.c_void_p,)
        tsdb_user_name.restype = ctypes.c_char_p

        result: bytes = tsdb_user_name(self._tsdb)
        return result.decode(encoding='utf-8')

    
    def get_db_current(self) -> str:
        tsdb_user_name = self._libdll.tsdb_v3_get_db_current
        tsdb_user_name.argtypes = (ctypes.c_void_p,)
        tsdb_user_name.restype = ctypes.c_char_p

        result: bytes = tsdb_user_name(self._tsdb)
        return result.decode(encoding='utf-8')

    # 
    def query(self, sql: str, charset: str = "", database: str = "") -> int:
        """[summary] execute sql query

        Args:
            sql (str): sql query statement
            charset (str, optional): character set. Defaults to None.
            database (str, optional): current database. Defaults to None.

        Returns:
            [int]: error number
        """
        charsetin = ""
        if charset:
            charsetin = charset
        else:
            charsetin = self._pool.get_charset()

        database = "" if not database else database

        func = self._libdll().tsdb_v3_query
        func.argtypes = (ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p,)
        func.restype = ctypes.c_int
        #  TODO: 如果sql语句中包含中文，但是没有指定utf-8编码，使用默认的Latin-1编码应该会有问题, 等待服务器适配之后进行处理
        return func(self._c_tsdb,
                          str2c_char_p(sql),
                          str2c_char_p(charsetin, encoding=charsetin),
                          str2c_char_p(database, encoding=charsetin),
                          )

    
    def query_reader(self, sql: str, charset: str = "", database: str = "",fetch_first_line:bool = False) -> c_void_p:
        """[summary] execute sql query

        Args:
            sql (str): sql query statement
            charset (str, optional): character set. Defaults to None.
            database (str, optional): current database. Defaults to None.

        Returns:
            [int]: error number
        """
        charsetin = ""
        if charset:
            charsetin = charset
        else:
            charsetin = self._pool.get_charset()

        database = "" if not database else database

        func = self._libdll().tsdb_v3_query_reader
        func.argtypes = (ctypes.c_void_p, ctypes.c_char_p,ctypes.c_char_p, ctypes.c_char_p,ctypes.c_bool,)
        func.restype = ctypes.c_void_p
        print("charset in: {}".format(charsetin))
        #  TODO: 如果sql语句中包含中文，但是没有指定utf-8编码，使用默认的Latin-1编码应该会有问题, 等待服务器适配之后进行处理
        c_reader = func(self._c_tsdb,
                    str2c_char_p(sql),
                    str2c_char_p(charsetin, encoding=charsetin),
                    str2c_char_p(database, encoding=charsetin),
                    fetch_first_line
                    )
        if not c_reader:
            return None
        return c_reader

    
    def store_result(self) -> c_void_p:
        func = self._libdll().tsdb_v3_store_result
        func.argtypes = (ctypes.c_void_p,)
        func.restype = ctypes.c_void_p
        c_reader = func(self._tsdb)
        if not c_reader:
            return None
        return c_reader

    
    def select_db(self,db_name:str) -> int:
        func = self._libdll().tsdb_v3_select_db
        func.argtypes = (ctypes.c_void_p,ctypes.c_char_p,)
        func.restype = ctypes.c_int
        return func(self._tsdb,str2c_char_p(db_name))