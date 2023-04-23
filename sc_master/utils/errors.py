from sc_master.utils.enums import ErrorCode


class ApiError(Exception):

    def __init__(self, *args):
        super().__init__(*args)

    def get_message(self) -> str:
        """
        Get error message
        :raise Exception: if message can't be obtained
        """
        raise Exception('Not implemented')

    def get_error_code(self) -> ErrorCode:
        """
        Get error code
        :raise Exception:  if code can't be obtained
        """
        raise Exception('Not implemented')

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


class DeviceClientError(ApiError):

    def __init__(
            self,
            device_address: str,
            device_port: int,
            command_name: str = None,
            captured_exception: Exception = None,
            client_error_status: int = None,
            client_error_message: str = None,
            client_error_result: dict = None):
        self._device_address = device_address
        self._device_port = device_port
        self._command_name = command_name
        self._captured_exception = captured_exception
        self._client_error_status = client_error_status
        self._client_error_message = client_error_message
        self._client_error_result = client_error_result

    def is_device_on(self) -> bool:
        # TODO: implementar 
        pass
    
    def get_error_code(self) -> ErrorCode:
        if self._command_name == 'connect':
            return ErrorCode.DE_ESTABLISHING_CONNECTION
        else:
            if self._captured_exception is not None:
                if isinstance(self._captured_exception, BrokenPipeError) or \
                        isinstance(self._captured_exception, ConnectionRefusedError):
                    return ErrorCode.DE_BROKEN_CONNECTION
                else:
                    return ErrorCode.GE_INTERNAL
            else:
                return ErrorCode.GE_INTERNAL

    def get_message(self) -> str:
        if self._command_name == 'connect':
            return f'Cannot establish connection with {self._device_address}:{self._device_port}'
        elif isinstance(self._captured_exception, BrokenPipeError):
            return f'BrokenPipeError when sending command to {self._device_address}:{self._device_port}'
        elif isinstance(self._captured_exception, ConnectionRefusedError):
            return f'ConnectionRefusedError when sending command to {self._device_address}:{self._device_port}'
        else:
            return f'Internal error when sending command to {self._device_address}:{self._device_port} see server logs'

    def get_device_address(self) -> str:
        return self._device_address

    def get_device_port(self) -> int:
        return self._device_port

    def __str__(self):
        if \
                self._client_error_status is not None and \
                self._client_error_message is not None and \
                self._client_error_result is not None:
            return f'Device on {self._device_address}:{self._device_port} returned :\
                \n\tstatus={self._client_error_status} \
                \n\tmessage={self._client_error_message} \
                \n\tresult={str(self._client_error_result)}'
        return super().__str__()
