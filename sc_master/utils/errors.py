from typing import Optional, Dict, Any
from sc_master.utils.enums import ErrorCode


class ApiError(Exception):

    def __init__(self, code: ErrorCode, message: Optional[str] = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.code = code
        self.message = message

    def __str__(self):
        return super().__str__()


class NotImplemented(Exception):

    def __init__(self, *args):
        super().__init__(*args)

    def get_message(self) -> str:
        """
        Get error message
        """
        return 'Internal error, see server logs.'

    def get_error_code(self) -> ErrorCode:
        """
        Get error code
        """
        return ErrorCode.INTERNAL_SERVER_ERROR


# TODO: instead of Dict[str, Any] define a dataclass for scp errors

class DeviceClientError(ApiError):

    def __init__(
            self,
            code: ErrorCode,
            exception: Optional[Exception] = None,
            scp_command: Optional[Dict[str, Any]] = None,
            scp_error: Optional[Dict[str, Any]] = None,
            *args,
            **kwargs):

        super().__init__(
            code if code is not None else ErrorCode.INTERNAL_SERVER_ERROR,
            self._get_message(code, exception, scp_command, scp_error),
            *args,
            **kwargs)
        self.exception = exception
        self.scp_command = scp_command
        self.scp_error = scp_error

    def _get_message(
            self,
            code: ErrorCode,
            exception: Optional[Exception] = None,
            scp_command: Optional[Dict[str, Any]] = None,
            scp_error: Optional[Dict[str, Any]] = None):

        if code == ErrorCode.SCP_ERROR:
            return f'Device returned "{scp_error}" for command "{scp_command}"'
        elif code == ErrorCode.SCP_TCP_ERROR_RECEIVING_RESPONSE:
            return f'Exception "{exception}" receiving response for command "{scp_command}"'
        elif code == ErrorCode.SCP_TCP_ERROR_SENDING_REQUEST:
            return f'Exception "{exception}" sending command "{scp_command}"'
        else:
            return None
