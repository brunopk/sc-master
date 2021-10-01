from enum import Enum


class HardwareMode(Enum):

    STATIC = 1

    def __str__(self) -> str:
        return self.name


class ErrorCode(Enum):

    DE_ESTABLISHING_CONNECTION = 101
    DE_BROKEN_CONNECTION = 102

    ST_OVERLAPPING = 201
    ST_NOT_FOUND = 202
    ST_EDITION_NOT_ALLOWED = 203

    SY_DEVICE_ALREADY_CONNECTED = 301
    SY_HAS_NO_CONNECTED_DEVICES = 302
    SY_TURNED_OFF = 303
    SY_MODE_ERROR = 304

    RE_NOT_FOUND = 401

    GE_INTERNAL = 1
    GE_CANNOT_CREATE_RESOURCE = 2
    GE_PARSE_ERROR = 3
    GE_BAD_REQUEST = 4

    def __int__(self):
        return self.value

    def __str__(self) -> str:
        return self.name
