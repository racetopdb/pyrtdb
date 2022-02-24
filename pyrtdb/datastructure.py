from enum import Enum
from enum import unique


@unique
class DataType(Enum):
    Unknown = 0
    Bool = 1
    Int = 2
    Int64 = 3
    Float = 4
    Double = 5
    Binary = 6
    String = 7
    Timestamp = 8   # datetime millistamp
    Pointer = 9
    TagString = 10