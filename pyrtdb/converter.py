from typing import Any
import datetime

from .exception import NotSupportedError, ProgrammingError


NoneType = type(None)
class Converter:
    def __init__(self) -> None:
        self.supporting_types = {
            int, float, NoneType, bool, datetime.date, datetime.datetime, str
        }

    def convert(self, o) -> Any:
        tp = type(o)
        if tp not in self.supporting_types:
            raise NotSupportedError("Converted type is not supported, type: {}".format(tp))
        try:
            if tp == str:
                return """'{}'""".format(o)
            elif tp == int:
                return self.any2str(o)
            elif tp == float:
                return self.float2str(o)
            elif tp == bool:
                return self.bool2str(o)
            elif tp == NoneType:
                return self.None2NULL(o)
            elif tp == datetime.datetime:
                return """'{}'""".format(datetime.datetime.strftime(o, "%Y-%m-%d %H:%M:%S.%f")[:-3])
            elif tp == datetime.datetime.date:
                return """'{}'""".format(datetime.date.strftime(o, "%Y-%m-%d"))
        except ValueError:
            raise ProgrammingError("Convert type failed, type: {}".format(tp))

    def float2str(self, o: float):
        s = repr(o)
        if s in ("inf", "nan"):
            raise ProgrammingError("{} can not be used with Rtdb".format(s))
        if "e" not in s:
            s += "e0"
        return s


    def None2NULL(self, o):
        return 'NULL'


    def bool2str(self, o: bool):
        return 'True' if o else 'False'


    def any2str(self, o: Any):
        return str(o)
