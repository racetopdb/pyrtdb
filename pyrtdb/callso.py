"""
Thid module implements part of the symbolic function packaging in the C language libstd.so.
All function names like "c_*" are the wrapped function of c language function.
"""
import platform
import ctypes
from ctypes import POINTER, Structure, c_int, c_void_p
from typing import Any, Callable, Iterable, List, Union
from functools import wraps
import sys

from .constant import CHARSET_DICT, LINUX_DLL_PATH, WIN32_DLL_PATH, X64_DLL_PATH
from .exception import handle_error, InterfaceError, NotSupportedError
from .datastructure import DataType
from .time import milli_timestamp2datetime


def err_handle_wrapper(func: Callable):
    """Process the error number returned by the database server and then raise the corresponding exception.

    Args:
        func (Callable): a funtion that returns an error number of database

    Returns:
        [type]: the wrapped function
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        errno = func(*args, **kwargs)
        handle_error(errno)
        return errno

    return wrapper


def load_linux_dll():
    return ctypes.CDLL(LINUX_DLL_PATH)


def load_mac_dll():
    raise NotSupportedError("Mac os is not supported.")


def load_windows32_dll():
    return ctypes.CDLL(WIN32_DLL_PATH)


def load_windows64_dll():
    return ctypes.CDLL(X64_DLL_PATH)


def load() -> Any:
    is_64bits = sys.maxsize > 2 ** 32
    system = platform.system()
    if system == 'Linux':
        return load_linux_dll()
    elif system == 'Windows':
        if is_64bits:
            return load_windows64_dll()
        else:
            return load_windows32_dll()
    elif system == 'Darwin':
        return load_mac_dll()
    else:
        raise OSError("unsupported operating system")


def str2c_char_p(s: str, encoding='utf-8') -> Any:
    # default encoding utf-8
    return ctypes.c_char_p(s.encode(encoding if encoding else 'utf-8'))


def c_char_p2str(ch: ctypes.c_char_p, encoding='utf-8') -> str:
    """Convert c language char pointer to python str.

    Args:
        ch (ctypes.c_char_p): string of c programming language
        encoding (str, optional): encoding. Defaults to 'utf-8'.

    Returns:
        str: python str

    """
    return ctypes.string_at(ch).decode(encoding=encoding if encoding else 'utf-8')


class Field(Structure):
    """Database column
    """
    _fields_ = [
        ('name', ctypes.c_char_p),
        ('field_index', ctypes.c_uint16),
        ('data_type', ctypes.c_byte, 4),
        ('unique', ctypes.c_byte, 1),
        ('has_index', ctypes.c_byte, 1),
        ('is_ref', ctypes.c_byte, 1),
        ('is_null', ctypes.c_byte, 1),
        ('length', ctypes.c_byte),
        ('field_id', ctypes.c_uint32),
        ('real_length', ctypes.c_byte),
        ('name_length', ctypes.c_byte),
        ('_reserved', ctypes.c_char * 2),
    ]


class Rows(Structure):
    pass


# If the _fields_ contains field of its own type, it must be defined outside the class.
Rows._fields_ = [
    ('next', POINTER(Rows)),
    ('row', POINTER(ctypes.c_void_p)),
    ('len', ctypes.c_uint64)
]


class ResultSet(Structure):
    _fields_ = [
        ('row_count', ctypes.c_uint64),
        ('field_count', ctypes.c_uint32),
        ('fields', ctypes.c_void_p),
        ('data', ctypes.c_void_p),
    ]


def convert_field(fields, fields_count) -> List[Field]:
    fields = ctypes.cast(fields, POINTER(POINTER(Field)))
    field_list = [fields[i].contents for i in range(fields_count)]

    return field_list


def get_field_value(value_pointer, value_type: int) -> Any:
    ctype = None
    if value_type == 0:
        return None
    value_type = abs(value_type)
    if value_type == DataType.String.value:
        return c_char_p2str(ctypes.cast(value_pointer, ctypes.c_char_p))
    if value_type == DataType.Bool.value:
        ctype = ctypes.c_bool
    elif value_type == DataType.Int.value:
        ctype = ctypes.c_int
    elif value_type == DataType.Int64.value:
        ctype = ctypes.c_int64
    elif value_type == DataType.Float.value:
        ctype = ctypes.c_float
    elif value_type == DataType.Double.value:
        ctype = ctypes.c_double
    elif value_type == DataType.Timestamp.value:
        ctype = ctypes.c_int64
        milli_timestamp = ctypes.cast(
            value_pointer, POINTER(ctype)).contents.value
        return milli_timestamp2datetime(milli_timestamp)

    # TODO: 现在不支持解析二进制数值
    # elif value_type == DataType.Binary.value:
    #     pass
    else:
        raise NotSupportedError("unsupported data type")

    return ctypes.cast(value_pointer, POINTER(ctype)).contents.value


class RawTsdbClientV2:
    def __init__(self, host: str, port: int, user: str, password: str, **kwargs):
        self.conn_str = self.__build_conn_str(user, password, host, port)
        self._libdll = load()
        self._tsdb = self.__new_tsdb()
        self._result: Union[c_void_p, None] = None
        self.charset = self.get_charset()

    def __build_conn_str(self, user: str, password: str, host: str, port: int) -> str:
        return "user={user};passwd={password};servers=tcp://{host}:{port}".format(
            user=user,
            password=password,
            host=host,
            port=port
        )

    @err_handle_wrapper
    def __new_tsdb(self) -> int:
        tsdb_new = self._libdll.tsdb_new
        tsdb_new.restype = ctypes.c_void_p

        return tsdb_new()

    @err_handle_wrapper
    def connect(self) -> int:
        tsdb_connect = self._libdll.tsdb_connect
        tsdb_connect.argtypes = (ctypes.c_char_p, )
        tsdb_connect.restype = ctypes.c_int
        return tsdb_connect(str2c_char_p(self.conn_str))

    @err_handle_wrapper
    def disconnect(self) -> int:
        tsdb_disconnect = self._libdll.tsdb_disconnect
        tsdb_disconnect.restype = ctypes.c_int
        return tsdb_disconnect()

    @err_handle_wrapper
    def set_charset(self, charset_id: int) -> int:
        charset = CHARSET_DICT.get(charset_id)
        if not charset:
            raise InterfaceError("not supported charset_id")
        # be optimistic that set charset is will execute successfully
        self.charset = charset
        tsdb_charset_set = self._libdll.tsdb_charset_set
        tsdb_charset_set.argtypes = (ctypes.c_char_p, )
        tsdb_charset_set.restype = ctypes.c_int

        return tsdb_charset_set(str2c_char_p(charset, encoding=self.charset))

    def get_charset(self) -> str:
        tsdb_charset_get = self._libdll.tsdb_charset_get
        tsdb_charset_get.restype = ctypes.c_char_p
        # If restype is c_char_p, it will convert to Python bytes type.
        result: bytes = tsdb_charset_get()

        return result.decode(encoding='utf-8')

    @err_handle_wrapper
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
        elif self.charset:
            charsetin = self.charset
        else:
            charsetin = self.charset = self.get_charset()

        database = "" if not database else database

        tsdb_query = self._libdll.tsdb_query
        tsdb_query.argtypes = (ctypes.c_void_p, ctypes.c_char_p,
                               ctypes.c_int, ctypes.c_char_p, ctypes.c_char_p, )
        tsdb_query.restype = ctypes.c_int
        print("charset in: {}".format(charsetin))
        #  TODO: 如果sql语句中包含中文，但是没有指定utf-8编码，使用默认的Latin-1编码应该会有问题, 等待服务器适配之后进行处理
        return tsdb_query(self._tsdb,
                          str2c_char_p(sql),
                          len(sql),
                          str2c_char_p(charsetin, encoding=charsetin),
                          str2c_char_p(database, encoding=charsetin),
                          )

    def store_result(self):
        tsdb_store_result_v2 = self._libdll.tsdb_store_result_v2
        tsdb_store_result_v2.argtypes = (ctypes.c_void_p, )
        tsdb_store_result_v2.restype = ctypes.c_void_p
        result = tsdb_store_result_v2(self._tsdb)
        self._result = result

    def free_result(self):
        if self._result:
            tsdb_free_result = self._libdll.tsdb_free_result
            tsdb_free_result.argtypes = (c_void_p, c_void_p, )
            tsdb_free_result.restypes = (c_int, )

            return tsdb_free_result(self._tsdb, self._result)

    def fetch_rows(self, rows_type: int = 0) -> Iterable:
        assert getattr(self, '_result')
        if not getattr(self, '_result') or not self._result:
            return []

        res_ptr = ctypes.cast(self._result, POINTER(ResultSet))
        fields_count = res_ptr.contents.field_count
        rows_count = res_ptr.contents.row_count
        if not fields_count or not rows_count:
            return []

        data = ctypes.cast(res_ptr.contents.data, POINTER(Rows))
        if not data:
            return []

        fields = convert_field(res_ptr.contents.fields, fields_count)
        field_name_list = [field.name.decode(encoding='utf-8') for field in fields]
        rows = []
        while(data != 0 and rows_count > 0):
            try:
                row = data.contents.row
                values = (get_field_value(
                    value_pointer=row[i], value_type=fields[i].data_type) for i in range(fields_count))
                data = data.contents.next
            except ValueError:
                # when foreach the end of linkedlist, catch ValueError: NULL pointer, then break.
                break
            if rows_type == 0:
                rows.append(tuple(values))
            elif rows_type == 1:
                rows.append({k: v for k, v in zip(field_name_list, values)})
            rows_count -= 1

        return rows

    @property
    def user_name(self) -> str:
        tsdb_user_name = self._libdll.tsdb_user_name
        tsdb_user_name.argtypes = (ctypes.c_void_p, )
        tsdb_user_name.restype = ctypes.c_char_p

        result: bytes = tsdb_user_name(self._tsdb)
        return result.decode(encoding='utf-8')

    def affected_rows(self) -> int:
        assert self._result
        res_ptr = ctypes.cast(self._result, POINTER(ResultSet))
        return res_ptr.contents.row_count

    @property
    def result(self):
        return self._result

    def kill_tsdb(self):
        if self._tsdb:
            tsbd_kill_me = self._libdll.tsdb_kill_me
            tsbd_kill_me.argtypes = (ctypes.c_void_p, )

            tsbd_kill_me(self._tsdb)
