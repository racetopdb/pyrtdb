
from .adaptor.rtdb_pool_v3 import rtdb_pool_v3
from .constant import *
from .rtdb import rtdb


class rtdb_pool(rtdb_pool_v3):
    def __init__(self,host: str, port: int, user: str, password: str, **kwargs):
        rtdb_pool_v3.__init__(self)
        self._host = host if host else RTDB_HOST
        self._port = port if port else RTDB_PORT
        self._user = user if user else RTDB_USER_NAME
        self._password = password if password else RTDB_PASSWORD

    def conn_url(self)->str:
        return self.build_conn_str(self._user,self._password,self._host,self._port)

    def newDB(self) -> rtdb:
        c_tsdb = rtdb_pool_v3.tsdb_v3_new(self)
        url = self.conn_url()
        return rtdb(self,c_tsdb,url)

