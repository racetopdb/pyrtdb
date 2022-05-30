from ctypes import c_void_p

from pyrtdb import rtdb_pool
from pyrtdb.adaptor.rtdb_field_v3 import rtdb_field_v3


class rtdb_field(rtdb_field_v3):
    def __init__(self, pool: rtdb_pool,c_field:c_void_p):
        rtdb_field_v3.__init__(self,pool,c_field)