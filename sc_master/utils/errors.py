from typing import Optional, Dict, Any, Union
from sc_master.utils.enums import ErrorCode


#TODO: agregar la causa del error (por ejemplo cuando da un error al mandar comando a sc-rpi) try to chain exceptions

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
        return ErrorCode.GE_INTERNAL


# TODO: simplify this class (remove get_error_code, just pass ErrorCode or exception and try to chain exceptions)
# TODO: diferenciar dos errores errores de scrpi , o errores de python (ej BrokenPipeError)
# TODO: instead of Dict[str, Any] define a dataclass for scp errors

class DeviceClientError(ApiError):

    def __init__(
            self,
            code: ErrorCode,
            inner_error: Union[Exception, Dict[str, Any]],
            scp_command: Optional[Dict[str, Any]] = None,
            address: Optional[str] = None,
            port: Optional[int] = None,
            *args,
            **kwargs):
        super().__init__(code if code is not None else ErrorCode.GE_INTERNAL, None, *args, **kwargs)
        self.inner_error = inner_error
        self.scp_command = scp_command
        self.address = address
        self.port = port
