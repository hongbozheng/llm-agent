import enum


class LogLevel(enum.Enum):
    ALL = 6
    TRACE = 5
    DEBUG = 4
    INFO = 3
    WARN = 2
    ERROR = 1
    FATAL = 0
    OFF = -1

    def __ge__(self, other):
        return isinstance(other, LogLevel) and self.value >= other.value

    def __gt__(self, other):
        return isinstance(other, LogLevel) and self.value > other.value

    def __le__(self, other):
        return isinstance(other, LogLevel) and self.value <= other.value

    def __lt__(self, other):
        return isinstance(other, LogLevel) and self.value < other.value
