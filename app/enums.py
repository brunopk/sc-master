from enum import Enum


class Error(Enum):

    BAD_REQUEST = 1
    SCRPI_CONNECTION_ERROR = 2
    SCRPI_SERVICE_ERROR = 3
    INTERNAL_SERVER_ERROR = 4
    INVALID_USER_OR_PASSWORD = 5
    RESOURCE_NOT_FOUND = 6
    CANNOT_CREATE_ELEMENT = 7

    def __str__(self):
        return self.name

    def __int__(self):
        return self.value
