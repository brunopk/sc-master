from enum import Enum


class ScRpiStatus(Enum):

    OK = 1
    HAS_ERROR = 2
    NOT_CONNECTED = 3

    def __str__(self):
        return self.name


class Error(Enum):

    BAD_REQUEST = 1
    SCRPI_CONNECTION_ERROR = 2
    SCRPI_SERVICE_ERROR = 3
    INTERNAL_SERVER_ERROR = 4
    INVALID_USER_OR_PASSWORD = 5
    RESOURCE_NOT_FOUND = 6
    CANNOT_CREATE_ELEMENT = 7
    PARSE_ERROR = 8
    SCRPI_BAD_PORT = 9
    SCRPI_CONNECTION_REFUSED = 10
    SCRPI_NOT_CONNECTED = 11
    SCRPI_BAD_ADDRESS = 12
    SECTION_OVERLAPPING = 13
    SECTION_NOT_IN_ACTIVE_STATIC_DESIGN = 14
    SECTION_IS_ALREADY_ON = 15
    SECTION_IS_ALREADY_OFF = 16
    STRIP_IS_ALREADY_ON = 17
    SECTION_NOT_DEFINED_OR_NOT_IN_ACTIVE_STATIC_DESIGN = 18
    STRIP_IS_ALREADY_OFF = 19

    def __str__(self):
        return self.name

    def __int__(self):
        return self.value
