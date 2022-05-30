from ctypes import  c_void_p

from pyrtdb import rtdb_pool, rtdb_field
from pyrtdb.adaptor.rtdb_reader_v3 import rtdb_reader_v3


class rtdb_reader(rtdb_reader_v3):
    def __init__(self, pool: rtdb_pool,c_reader:c_void_p):
        rtdb_reader_v3.__init__(self,pool,c_reader)

    def field_get(self, field_index: int) -> rtdb_field:
        c_field = rtdb_reader_v3.field_get(field_index)
        if not c_field:
            return None
        return rtdb_field(self.pool(),c_field)

    def field_find(self, field_name: str) -> rtdb_field:
        c_field = rtdb_reader_v3.field_find(field_name)
        if not c_field:
            return None
        return rtdb_field(self.pool(),c_field)