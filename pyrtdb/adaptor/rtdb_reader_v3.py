import ctypes
from ctypes import Union,POINTER, Structure, c_int, c_void_p

from pyrtdb.adaptor.rtdb_pool_v3 import rtdb_pool_v3
from pyrtdb.adaptor.so import  str2c_char_p

class rtdb_reader_v3:
    def __init__(self, pool: rtdb_pool_v3,c_reader:c_void_p):
        self._pool = pool
        self._c_reader = c_reader

    def _libdll(self):
        return self._pool.libdll()

    def pool(self):
        return self._pool

    
    def kill_me(self):
        func = self._libdll().tsdb_v3_reader_kill_me
        func.argtypes = (ctypes.c_void_p,)
        func(self._c_reader)
        self._c_reader = None

    
    def open(self,conn_url:str)-> int:
        func = self._libdll().tsdb_v3_reader_open
        func.argtypes = (ctypes.c_void_p,ctypes.c_char_p,)
        func.restype = ctypes.c_int
        return func(self._c_reader,str2c_char_p(conn_url))

    
    def query(self, sql: str) -> int:
        func = self._libdll().tsdb_v3_reader_query
        func.argtypes = (ctypes.c_void_p, ctypes.c_char_p,)
        func.restype = ctypes.c_int
        return func(self._c_reader, str2c_char_p(sql))

    
    def get_field_count(self) -> int:
        func = self._libdll().tsdb_v3_reader_get_field_count
        func.argtypes = (ctypes.c_void_p,)
        func.restype = ctypes.c_int
        return func(self._c_reader)

    
    def field_add(self, field_name: str,data_type:int,length:int,is_null:bool) -> int:
        charsetin = self._pool.get_charset()
        func = self._libdll().tsdb_v3_reader_field_add
        func.argtypes = (ctypes.c_void_p,ctypes.c_char_p,ctypes.c_int,ctypes.c_int,ctypes.c_bool,)
        func.restype = ctypes.c_int
        return func(self._c_reader,str2c_char_p(field_name, encoding=charsetin),data_type,length,is_null)

    
    def get_row_count(self) -> int:
        func = self._libdll().tsdb_v3_reader_get_row_count
        func.argtypes = (ctypes.c_void_p,)
        func.restype = ctypes.c_uint64
        return func(self._c_reader)

    
    def cursor_next(self) -> int:
        func = self._libdll().tsdb_v3_reader_cursor_next
        func.argtypes = (ctypes.c_void_p,)
        func.restype = ctypes.c_int
        return func(self._c_reader)

    
    def cursor_set(self,row_index:int) -> int:
        func = self._libdll().tsdb_v3_reader_cursor_set
        func.argtypes = (ctypes.c_void_p,ctypes.c_uint64)
        func.restype = ctypes.c_int
        return func(self._c_reader,row_index)

    
    def cursor_reset(self) -> int:
        func = self._libdll().tsdb_v3_reader_cursor_reset
        func.argtypes = (ctypes.c_void_p,)
        func.restype = ctypes.c_int
        return func(self._c_reader)

    
    def clear(self,clear_data:bool,clear_field:bool):
        func = self._libdll().tsdb_v3_reader_clear
        func.argtypes = (ctypes.c_void_p,ctypes.c_bool,ctypes.c_bool,)
        return func(self._c_reader,clear_data,clear_field)

    
    def is_null(self, field_index: int) -> bool:
        func = self._libdll().tsdb_v3_reader_is_null
        func.argtypes = (ctypes.c_void_p, ctypes.c_uint32,)
        func.restype = ctypes.c_bool
        return func(self._c_reader, field_index)

    
    def is_null_s(self, field_name: str) -> bool:
        charsetin = self._pool.get_charset()
        func = self._libdll().tsdb_v3_reader_is_null_s
        func.argtypes = (ctypes.c_void_p, ctypes.c_char_p,)
        func.restype = ctypes.c_bool
        return func(self._c_reader, str2c_char_p(field_name, encoding=charsetin))

    
    def get_bool(self, field_index:int) -> bool:
        func = self._libdll().tsdb_v3_reader_get_bool
        func.argtypes = (ctypes.c_void_p, ctypes.c_uint32,)
        func.restype = ctypes.c_bool
        return func(self._c_reader, field_index)

    
    def get_bool_s(self, field_name: str) -> bool:
        charsetin = self._pool.get_charset()
        func = self._libdll().tsdb_v3_reader_get_bool_s
        func.argtypes = (ctypes.c_void_p, ctypes.c_char_p,)
        func.restype = ctypes.c_bool
        return func(self._c_reader, str2c_char_p(field_name, encoding=charsetin))

    def get_int(self, field_index: int) -> int:
        func = self._libdll().tsdb_v3_reader_get_int
        func.argtypes = (ctypes.c_void_p, ctypes.c_uint32,)
        func.restype = ctypes.c_int
        return func(self._c_reader, field_index)

    def get_int_s(self, field_name: str) -> int:
        charsetin = self._pool.get_charset()
        func = self._libdll().tsdb_v3_reader_get_int_s
        func.argtypes = (ctypes.c_void_p, ctypes.c_char_p,)
        func.restype = ctypes.c_int
        return func(self._c_reader, str2c_char_p(field_name, encoding=charsetin))

    def get_int64(self, field_index: int) -> int:
        func = self._libdll().tsdb_v3_reader_get_int64
        func.argtypes = (ctypes.c_void_p, ctypes.c_uint32,)
        func.restype = ctypes.c_int64
        return func(self._c_reader, field_index)

    def get_int64_s(self, field_name: str) -> int:
        charsetin = self._pool.get_charset()
        func = self._libdll().tsdb_v3_reader_get_int64_s
        func.argtypes = (ctypes.c_void_p, ctypes.c_char_p,)
        func.restype = ctypes.c_int64
        return func(self._c_reader, str2c_char_p(field_name, encoding=charsetin))

    def get_datetime_ms(self, field_index: int) -> int:
        func = self._libdll().tsdb_v3_reader_get_datetime_ms
        func.argtypes = (ctypes.c_void_p, ctypes.c_uint32,)
        func.restype = ctypes.c_int64
        return func(self._c_reader, field_index)

    def get_datetime_ms_s(self, field_name: str) -> int:
        charsetin = self._pool.get_charset()
        func = self._libdll().tsdb_v3_reader_get_datetime_ms_s
        func.argtypes = (ctypes.c_void_p, ctypes.c_char_p,)
        func.restype = ctypes.c_int64
        return func(self._c_reader, str2c_char_p(field_name, encoding=charsetin))

    def get_float(self, field_index: int) -> float:
        func = self._libdll().tsdb_v3_reader_get_float
        func.argtypes = (ctypes.c_void_p, ctypes.c_uint32,)
        func.restype = ctypes.c_float
        return func(self._c_reader, field_index)

    def get_float_s(self, field_name: str) -> float:
        charsetin = self._pool.get_charset()
        func = self._libdll().tsdb_v3_reader_get_float_s
        func.argtypes = (ctypes.c_void_p, ctypes.c_char_p,)
        func.restype = ctypes.c_float
        return func(self._c_reader, str2c_char_p(field_name, encoding=charsetin))

    def get_double(self, field_index: int) -> float:
        func = self._libdll().tsdb_v3_reader_get_double
        func.argtypes = (ctypes.c_void_p, ctypes.c_uint32,)
        func.restype = ctypes.c_double
        return func(self._c_reader, field_index)

    def get_double_s(self, field_name: str) -> float:
        charsetin = self._pool.get_charset()
        func = self._libdll().tsdb_v3_reader_get_double_s
        func.argtypes = (ctypes.c_void_p, ctypes.c_char_p,)
        func.restype = ctypes.c_double
        return func(self._c_reader, str2c_char_p(field_name, encoding=charsetin))

    def get_string(self, field_index: int) -> str:
        func = self._libdll().tsdb_v3_reader_get_string
        func.argtypes = (ctypes.c_void_p, ctypes.c_uint32,ctypes.c_void_p,)
        func.restype = ctypes.c_char_p
        len = c_int(0)
        c_str: bytes = func(self._c_reader, field_index,ctypes.byref(len))
        if not c_str:
            return ""
        return c_str.decode(encoding='utf-8')

    def get_string_s(self, field_name: str) -> str:
        charsetin = self._pool.get_charset()
        func = self._libdll().tsdb_v3_reader_get_string_s
        func.argtypes = (ctypes.c_void_p, ctypes.c_char_p, ctypes.c_void_p,)
        func.restype = ctypes.c_char_p
        len = c_int(0)
        c_str: bytes = func(self._c_reader, str2c_char_p(field_name, encoding=charsetin), ctypes.byref(len))
        if not c_str:
            return ""
        return c_str.decode(encoding='utf-8')

    
    def row_add(self) -> int:
        func = self._libdll().tsdb_v3_reader_row_add
        func.argtypes = (ctypes.c_void_p,)
        func.restype = ctypes.c_int
        return func(self._c_reader)

    
    def set_null(self, field_index: int) -> int:
        func = self._libdll().tsdb_v3_reader_set_null
        func.argtypes = (ctypes.c_void_p, ctypes.c_uint32,)
        func.restype = ctypes.c_int
        return func(self._c_reader, field_index)

    
    def set_bool(self, field_index: int,v:bool) -> int:
        func = self._libdll().tsdb_v3_reader_set_bool
        func.argtypes = (ctypes.c_void_p, ctypes.c_uint32,ctypes.c_bool,)
        func.restype = ctypes.c_int
        return func(self._c_reader, field_index,v)

    
    def set_int(self, field_index: int, v: int) -> int:
        func = self._libdll().tsdb_v3_reader_set_int
        func.argtypes = (ctypes.c_void_p, ctypes.c_uint32, ctypes.c_int,)
        func.restype = ctypes.c_int
        return func(self._c_reader, field_index, v)

    
    def set_int64(self, field_index: int, v: int) -> int:
        func = self._libdll().tsdb_v3_reader_set_int64
        func.argtypes = (ctypes.c_void_p, ctypes.c_uint32, ctypes.c_int64,)
        func.restype = ctypes.c_int
        return func(self._c_reader, field_index, v)

    
    def set_datetime_ms(self, field_index: int, v: int) -> int:
        func = self._libdll().tsdb_v3_reader_set_datetime_ms
        func.argtypes = (ctypes.c_void_p, ctypes.c_uint32, ctypes.c_int64,)
        func.restype = ctypes.c_int
        return func(self._c_reader, field_index, v)

    
    def set_float(self, field_index: int, v: float) -> int:
        func = self._libdll().tsdb_v3_reader_set_float
        func.argtypes = (ctypes.c_void_p, ctypes.c_uint32, ctypes.c_float,)
        func.restype = ctypes.c_int
        return func(self._c_reader, field_index, v)

    
    def set_double(self, field_index: int, v: float) -> int:
        func = self._libdll().tsdb_v3_reader_set_double
        func.argtypes = (ctypes.c_void_p, ctypes.c_uint32, ctypes.c_double,)
        func.restype = ctypes.c_int
        return func(self._c_reader, field_index, v)

    
    def set_string(self, field_index: int, v: str) -> int:
        func = self._libdll().tsdb_v3_reader_set_string
        func.argtypes = (ctypes.c_void_p, ctypes.c_uint32, ctypes.c_char_p,ctypes.c_uint32,)
        func.restype = ctypes.c_int
        return func(self._c_reader, field_index, str2c_char_p(v),len(v))

    
    def set_row_from(self,from_reader: "rtdb_reader_v3") -> int:
        func = self._libdll().tsdb_v3_reader_set_row_from
        func.argtypes = (ctypes.c_void_p, ctypes.c_void_p,)
        func.restype = ctypes.c_int
        return func(self._c_reader, from_reader._c_reader)

    
    def row_add_commit(self) -> int:
        func = self._libdll().tsdb_v3_reader_row_add_commit
        func.argtypes = (ctypes.c_void_p,)
        func.restype = ctypes.c_int
        return func(self._c_reader)

    
    def select_db(self, db_name: str) -> int:
        func = self._libdll().tsdb_v3_select_db
        func.argtypes = (ctypes.c_void_p, ctypes.c_char_p,)
        func.restype = ctypes.c_int
        return func(self._c_reader, str2c_char_p(db_name))

    
    def field_get(self, field_index: int) -> c_void_p:
        func = self._libdll().tsdb_v3_reader_field_get
        func.argtypes = (ctypes.c_void_p, ctypes.c_uint32,)
        func.restype = ctypes.c_void_p
        c_field = func(self._c_reader, field_index)
        if not c_field:
            return None
        return c_field

    
    def field_find(self, field_name: str) -> c_void_p:
        charsetin = self._pool.get_charset()
        func = self._libdll().tsdb_v3_reader_field_find
        func.argtypes = (ctypes.c_void_p, ctypes.c_char_p,)
        func.restype = ctypes.c_void_p
        c_field = func(self._c_reader, str2c_char_p(field_name, encoding=charsetin))
        if not c_field:
            return None
        return c_field