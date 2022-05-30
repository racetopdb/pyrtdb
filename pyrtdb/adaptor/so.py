"""
Thid module implements part of the symbolic function packaging in the C language libstd.so.
All function names like "c_*" are the wrapped function of c language function.
"""
import platform
import ctypes
from typing import Any
import sys

from pyrtdb.constant import LINUX_DLL_PATH, WIN32_DLL_PATH, X64_DLL_PATH
from pyrtdb.exception import NotSupportedError


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
