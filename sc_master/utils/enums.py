from enum import Enum


class HardwareMode(Enum):

    STATIC = 1

    def __str__(self) -> str:
        return self.name


class ErrorCode(Enum):

    SCP_ERROR = 101
    SCP_TCP_ERROR_SENDING_REQUEST = 102
    SCP_TCP_ERROR_RECEIVING_RESPONSE = 103
    SCP_TCP_CONNECTION_ERROR = 104

    ST_OVERLAPPING = 201
    SECTION_NOT_FOUND = 202
    ST_EDITION_NOT_ALLOWED = 203
    SECTION_ALREADY_ON = 204
    SECTION_ALREADY_OFF = 205

    SY_DEVICE_ALREADY_CONNECTED = 301
    SY_HAS_NO_CONNECTED_DEVICES = 302
    SY_TURNED_OFF = 303
    SY_MODE_ERROR = 304
    LIGHTS_ALREADY_ON = 305
    LIGHTS_ALREADY_OFF = 306

    RE_NOT_FOUND = 401

    INTERNAL_SERVER_ERROR = 1
    GE_CANNOT_CREATE_RESOURCE = 2
    GE_PARSE_ERROR = 3
    GE_BAD_REQUEST = 4

    def __int__(self):
        return self.value

    def __str__(self) -> str:
        return self.name
