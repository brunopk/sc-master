from enum import Enum


class Error(Enum):

    BAD_REQUEST = 1
    SCDRIVER_DISCONNECTED = 2
    SCDRIVER_SERVICE_ERROR = 3
    INTERNAL_SERVER_ERROR = 4
    INVALID_USER_OR_PASSWORD = 5

    def __str__(self):
        return self.name

    def __int__(self):
        return self.value
