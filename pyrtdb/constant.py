from enum import Enum, unique
from pathlib import Path

# Default config
RTDB_USER_NAME = "test"
RTDB_HOST = "127.0.0.1"
RTDB_PORT = 9000
RTDB_PASSWORD = "test"
DEBUG_PRINT_SQL = True

# Error number
EPERM = 1  # Operation not permitted * /
ENOENT = 2  # No such file or directory * /
ESRCH = 3  # No such process * /
EINTR = 4  # Interrupted system call * /
EIO = 5  # I/O error * /
ENXIO = 6  # No such device or address * /
E2BIG = 7  # Argument list too long * /
ENOEXEC = 8  # Exec format error * /
EBADF = 9  # Bad file number * /
ECHILD = 10  # No child processes * /
EAGAIN = 11  # Try again * /
ENOMEM = 12  # Out of memory * /
EACCES = 13  # Permission denied * /
EFAULT = 14  # Bad address * /
ENOTBLK = 15  # Block device required * /
EBUSY = 16  # Device or resource busy * /
EEXIST = 17  # File exists * /
EXDEV = 18  # Cross-device link * /
ENODEV = 19  # No such device * /
ENOTDIR = 20  # Not a directory * /
EISDIR = 21  # Is a directory * /
EINVAL = 22  # Invalid argument * /
ENFILE = 23  # File table overflow * /
EMFILE = 24  # Too many open files * /
ENOTTY = 25  # Not a typewriter * /
ETXTBSY = 26  # Text file busy * /
EFBIG = 27  # File too large * /
ENOSPC = 28  # No space left on device * /
ESPIPE = 29  # Illegal seek * /
EROFS = 30  # Read-only file system * /
EMLINK = 31  # Too many links * /
EPIPE = 32  # Broken pipe * /
EDOM = 33  # Math argument out of domain of func * /
ERANGE = 34  # Math result not representable * /

MAX_ERRNO = ERANGE  # if modified error number, must modify this

# Charset
CHARSET_UNKNOWN = ""
CHARSET_GBK = "gbk"
CHARSET_UTF8 = "utf-8"
CHARSET_UCS2LE = "ucs-2le"
CHARSET_UCS2BE = "ucs-2be"
CHARSET_BIG5 = "big-5"
CHARSET_EUCJP = "euc-jp"
CHARSET_SJIS = "shift-jis"
CHARSET_EUCKR = "euc-kr"
CHARSET_ISO1 = "iso-8859-1"
CHARSET_WIN1 = "windows-1251"
CHARSET_WIN2 = "windows-1252"


# Charset id
@unique
class CharsetID(Enum):
    CHARSET_UNKNOWN = 0
    CHARSET_GBK = 1
    CHARSET_UTF8 = 2
    CHARSET_UCS2LE = 3
    CHARSET_UCS2BE = 4
    CHARSET_BIG5 = 5
    CHARSET_EUCJP = 6
    CHARSET_SJIS = 7
    CHARSET_EUCKR = 8
    CHARSET_ISO1 = 9
    CHARSET_WIN1 = 10
    CHARSET_WIN2 = 11


CHARSET_DICT = {
    CharsetID.CHARSET_UNKNOWN.value: CHARSET_UNKNOWN,
    CharsetID.CHARSET_GBK.value: CHARSET_GBK,
    CharsetID.CHARSET_UTF8.value: CHARSET_UTF8,
    CharsetID.CHARSET_UCS2LE.value: CHARSET_UCS2LE,
    CharsetID.CHARSET_UCS2BE.value: CHARSET_UCS2BE,
    CharsetID.CHARSET_BIG5.value: CHARSET_BIG5,
    CharsetID.CHARSET_EUCJP.value: CHARSET_EUCJP,
    CharsetID.CHARSET_SJIS.value: CHARSET_SJIS,
    CharsetID.CHARSET_EUCKR.value: CHARSET_EUCKR,
    CharsetID.CHARSET_ISO1.value: CHARSET_ISO1,
    CharsetID.CHARSET_WIN1.value: CHARSET_WIN1,
    CharsetID.CHARSET_WIN2.value: CHARSET_WIN2,
}

# Path of dynamic link library, supporting Linux, Win32(Windows 32bits), x64(Windows 64bits)
# supporting absolute path or relative path.
DLL_PATH = Path(Path(__file__).parent.absolute(), "dll")
LINUX_DLL_PATH = str(Path(DLL_PATH, "linux", "libtsdb.so").absolute())
WIN32_DLL_PATH = str(Path(DLL_PATH, "windows", "win32", "tsdb.dll").absolute())
X64_DLL_PATH = str(Path(DLL_PATH, "windows", "x64", "tsdb.dll").absolute())