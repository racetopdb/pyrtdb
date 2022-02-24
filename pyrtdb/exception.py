"""Exception classes for rtdb.

Details can be seen at https://www.python.org/dev/peps/pep-0249/.
"""


from .constant import *


class RtdbError(Exception):
    """Exception related to operation with Rtdb."""
    pass


class Warning(Warning, RtdbError):
    """Exception raised for important warnings like data truncations while inserting, etc. It must be a subclass of the Python StandardError (defined in the module exceptions)."""
    pass


class InterfaceError(RtdbError):
    """Exception raised for errors that are related to the database interface rather than the database itself. It must be a subclass of Error."""
    pass


class DatabaseError(RtdbError):
    """Exception raised for errors that are related to the database. It must be a subclass of Error."""
    pass


class InternalError(DatabaseError):
    """Exception raised when the database encounters an internal error, e.g. the cursor is not valid anymore, the transaction is out of sync, etc. It must be a subclass of DatabaseError."""
    pass


class OperationalError(DatabaseError):
    """
    Exception raised for errors that are related to the database's operation and not necessarily under the control of the programmer, 
    e.g. an unexpected disconnect occurs, the data source name is not found, a transaction could not be processed, a memory allocation error occurred during processing, etc. 
    It must be a subclass of DatabaseError.
    """
    pass


class ProgrammingError(DatabaseError):
    """
    Exception raised for programming errors, e.g. table not found or already exists, syntax error in the SQL statement, wrong number of parameters specified, etc. 
    It must be a subclass of DatabaseError.
    """
    pass


class IntegrityError(DatabaseError):
    """
    Exception raised when the relational integrity of the database is affected, e.g. a foreign key check fails.
    It must be a subclass of DatabaseError.
    """
    pass


class DataError(DatabaseError):
    """
    Exception raised for errors that are due to problems with the processed data like division by zero, numeric value out of range, etc. 
    It must be a subclass of DatabaseError.
    """
    pass


class NotSupportedError(DatabaseError):
    """
    Exception raised in case a method or database API was used which is not supported by the database, e.g. requesting a .rollback() on a connection that does not support transaction or has transactions turned off.
    It must be a subclass of DatabaseError.
    """
    pass


class InvalidArgs(ProgrammingError, ValueError):
    """
    Exception raised when the parameters passed in is invalid.
    It's a subclass of ProgrammingError.
    """
    pass


def handle_error(errno: int):
    min_errno = 0
    if errno <= min_errno or errno > MAX_ERRNO:
        return

    if errno == EINVAL:
        raise InvalidArgs("invalid args, please check your input")
    elif errno == EFAULT:
        raise OperationalError("maybe segment fault")
    elif errno == EEXIST:
        raise ProgrammingError("the database exists or table already exists")
    elif errno == ENOMEM:
        raise DatabaseError("database server out of memory")
    elif errno == ENOENT:
        raise DatabaseError("the current database does not exist or the current table does not exist")
    elif errno == EACCES:
        raise DatabaseError(
            "insufficient privileges to access the database for certain operations")
    else:
        raise DatabaseError("database error number: {}".format(errno))
