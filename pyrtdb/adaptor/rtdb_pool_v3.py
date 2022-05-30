import ctypes
from ctypes import c_int, c_void_p

import pyrtdb
from pyrtdb.adaptor.so import load, str2c_char_p
from pyrtdb.constant import CHARSET_DICT

TSDB_V3_VERSION  =  202204140917

class rtdb_pool_v3:
    def __init__(self):
        self._libdll = load()

    def libdll(self):
        return self._libdll;

    def build_conn_str(self, user: str, password: str, host: str, port: int) -> str:
        return "user={user};passwd={password};servers=tcp://{host}:{port}".format(
            user=user,
            password=password,
            host=host,
            port=port
        )

    
    def tsdb_v3_new(self) -> c_void_p:
        func = self._libdll.tsdb_v3_new
        func.argtypes = (ctypes.c_int64,)
        func.restype = ctypes.c_void_p

        return func(TSDB_V3_VERSION)


    
    def tsdb_v3_tls(self) ->c_void_p:
        func_tsdb_tls = self._libdll.tsdb_v3_tls
        func_tsdb_tls.argtypes = (ctypes.c_int64,)
        func_tsdb_tls.restype = ctypes.c_void_p
        return func_tsdb_tls(TSDB_V3_VERSION)

    
    def get_base_dir(self, add_path_sep: bool) -> str:
        func = self._libdll.tsdb_v3_get_base_dir
        func.argtypes = (ctypes.c_char_p, ctypes.c_void_p, ctypes.c_bool,)
        func.restype = ctypes.c_bool
        dir = ctypes.create_string_buffer(256)
        dir_len = c_int(256)
        ok = func(ctypes.byref(dir), ctypes.byref(dir_len), add_path_sep)
        if ok:
            return dir.decode(encoding='utf-8')
        return ""

    
    def get_log_dir(self, add_path_sep: bool) -> str:
        func = self._libdll.tsdb_v3_get_log_dir
        func.argtypes = (ctypes.c_char_p, ctypes.c_void_p, ctypes.c_bool,)
        func.restype = ctypes.c_bool
        dir = ctypes.create_string_buffer(256)
        dir_len = c_int(256)
        ok = func(ctypes.byref(dir), ctypes.byref(dir_len), add_path_sep)
        if ok:
            return dir.decode(encoding='utf-8')
        return ""

    
    def is_logined(self) -> bool:
        func = self._libdll.tsdb_v3_is_logined
        func.restype = ctypes.c_bool
        return func()

    # 
    def get_charset(self) -> str:
        func = self._libdll.tsdb_v3_get_charset
        func.restype = ctypes.c_char_p
        # If restype is c_char_p, it will convert to Python bytes type.
        result: bytes = func()

        st = result.decode(encoding='utf-8')
        return st

    
    def set_charset(self, charset_id: int) -> int:
        charset = CHARSET_DICT.get(charset_id)
        if not charset:
            raise pyrtdb.InterfaceError("not supported charset_id")
        # be optimistic that set charset is will execute successfully
        func = self._libdll.tsdb_v3_set_charset
        func.argtypes = (ctypes.c_char_p,)
        func.restype = ctypes.c_int
        return func(str2c_char_p(charset, encoding=self.charset))

    
    def set_timeout(self,connect_timeout_ms:int,send_timeout_ms:int,recv_timeout_ms:int) -> int:
        func = self._libdll.tsdb_v3_set_timeout
        func.argtypes = (ctypes.c_int,ctypes.c_int,ctypes.c_int,)
        func.restype = ctypes.c_int
        return func(connect_timeout_ms,send_timeout_ms,recv_timeout_ms)

    
    def get_timeout_connect(self) -> int:
        func = self._libdll.tsdb_v3_get_timeout_connect
        func.restype = ctypes.c_int
        return func()

    
    def get_timeout_send(self) -> int:
        func = self._libdll.tsdb_v3_get_timeout_send
        func.restype = ctypes.c_int
        return func()

    
    def get_timeout_recv(self) -> int:
        func = self._libdll.tsdb_v3_get_timeout_recv
        func.restype = ctypes.c_int
        return func()