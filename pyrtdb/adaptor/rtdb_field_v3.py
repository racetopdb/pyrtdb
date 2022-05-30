import ctypes
from ctypes import c_void_p
from pyrtdb.adaptor.rtdb_pool_v3 import rtdb_pool_v3

class rtdb_field_v3:
    def __init__(self, pool: rtdb_pool_v3,c_field:c_void_p):
        self._pool = pool
        self._c_field = c_field

    def _libdll(self):
        return self._pool.libdll()

    def pool(self):
        return self._pool

    
    def name(self) -> str:
        func = self._libdll().tsdb_v3_field_name
        func.argtypes = (ctypes.c_void_p,)
        func.restype = ctypes.c_char_p
        # If restype is c_char_p, it will convert to Python bytes type.
        result: bytes = func(self._c_field)
        return result.decode(encoding='utf-8')

    
    def index(self) -> int:
        func = self._libdll().tsdb_v3_field_index
        func.argtypes = (ctypes.c_void_p,)
        func.restype = ctypes.c_int
        return func(self._c_field)

    
    def data_type(self) -> int:
        func = self._libdll().tsdb_v3_field_data_type
        func.argtypes = (ctypes.c_void_p,)
        func.restype = ctypes.c_int
        return func(self._c_field)

    
    def is_unique(self) -> bool:
        func = self._libdll().tsdb_v3_field_is_unique
        func.argtypes = (ctypes.c_void_p,)
        func.restype = ctypes.c_bool
        return func(self._c_field)

    
    def is_ref(self) -> bool:
        func = self._libdll().tsdb_v3_field_is_ref
        func.argtypes = (ctypes.c_void_p,)
        func.restype = ctypes.c_bool
        return func(self._c_field)

    
    def is_null(self) -> bool:
        func = self._libdll().tsdb_v3_field_is_null
        func.argtypes = (ctypes.c_void_p,)
        func.restype = ctypes.c_bool
        return func(self._c_field)

    
    def size(self) -> int:
        func = self._libdll().tsdb_v3_field_length
        func.argtypes = (ctypes.c_void_p,)
        func.restype = ctypes.c_int
        return func(self._c_field)

    
    def length(self) -> int:
        func = self._libdll().tsdb_v3_field_real_length
        func.argtypes = (ctypes.c_void_p,)
        func.restype = ctypes.c_int
        return func(self._c_field)

    
    def field_id(self) -> int:
        func = self._libdll().tsdb_v3_field_id
        func.argtypes = (ctypes.c_void_p,)
        func.restype = ctypes.c_uint32
        return func(self._c_field)