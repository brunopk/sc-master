import traceback
from functools import wraps
from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import ParseError
from django.http.response import Http404
from django.db.utils import IntegrityError
from django.db.models import ObjectDoesNotExist  # type: ignore
from logging import getLogger
from sc_master.serializers.error import Error as ErrorSerializer
from sc_master.utils.errors import ApiError, DeviceClientError
from sc_master.utils.enums import ErrorCode
from sc_master.utils.helpers import map_error_code_to_http_status

logger = getLogger(__name__)


def catch_errors():

    def pretty_log_device_client_error(error: DeviceClientError): 
        if error.code == ErrorCode.SCP_ERROR:
            logger.error(f'\n\
                            \r--------------------------------------------\n\
                            \rDevice return {error.scp_error}             \n\
                            \rAfter executing command {error.scp_command} \n\
                            \r--------------------------------------------\n')
        elif error.code == ErrorCode.SCP_TCP_CONNECTION_ERROR:
            logger.error(f'\n\
                            \r-------------------------------------------------------------------\n\
                            \rError {error.exception} trying to establish connection with device \n\
                            \r-------------------------------------------------------------------\n')
        elif error.code == ErrorCode.SCP_TCP_ERROR_SENDING_REQUEST:
            logger.error(f'\n\
                            \r------------------------------------------------\n\
                            \rError {error.exception}                         \n\
                            \rSending request for command {error.scp_command} \n\
                            \r------------------------------------------------\n')
        elif error.code == ErrorCode.SCP_TCP_ERROR_RECEIVING_RESPONSE:
            logger.error(f'\n\
                            \r---------------------------------------------------\r\
                            \rError {error.exception}                            \r\
                            \rReceiving response for command {error.scp_command} \r\
                            \r---------------------------------------------------\r')

    def decorator(view_func):

        # noinspection PyBroadException
        @wraps(view_func)
        def _wrapped_view_func(self, request, *args, **kwargs):

            _status = None
            _error = None
            _is_error = False

            # self is the instance of the class with the decorated method
            try:
                return view_func(self, request, *args, **kwargs)

            except DeviceClientError as ex:
                try:
                    logger.exception(ex)
                    pretty_log_device_client_error(ex)
                    _is_error = True
                    _serializer_data = {
                        'code': ex.code,
                        'message': ex.message
                    }
                    _status = map_error_code_to_http_status(ex.code)
                    _error = ErrorSerializer(_serializer_data)
                except Exception as ex:
                    logger.exception(ex)

            # for instance when violating model attribute unique constraint
            except IntegrityError as ex:
                try:
                    logger.exception(ex)
                    _is_error = True
                    _status = map_error_code_to_http_status(ErrorCode.GE_CANNOT_CREATE_RESOURCE)
                    _error = ErrorSerializer({
                        'code': ErrorCode.GE_CANNOT_CREATE_RESOURCE,
                        'message': f'Cannot create resource {ex}.',
                    })
                except Exception as ex:
                    logger.exception(ex)

            except ParseError as ex:
                try:
                    logger.exception(ex)
                    _is_error = True
                    _status = map_error_code_to_http_status(ErrorCode.GE_PARSE_ERROR)
                    _error = ErrorSerializer({
                        'code': ErrorCode.GE_PARSE_ERROR,
                        'message': 'Cannot parse request.',
                    })
                except Exception as ex:
                    logger.exception(ex)

            except Http404 as ex:
                try:
                    logger.exception(ex)
                    _is_error = True
                    _status = map_error_code_to_http_status(ErrorCode.RE_NOT_FOUND)
                    _error = ErrorSerializer({
                        'code': ErrorCode.RE_NOT_FOUND,
                        'message': f'Resource not found {ex}.',
                    })
                except Exception as ex:
                    logger.exception(ex)

            except ObjectDoesNotExist as ex:
                try:
                    logger.exception(ex)
                    _is_error = True
                    _status = map_error_code_to_http_status(ErrorCode.RE_NOT_FOUND)
                    _error = ErrorSerializer({'code': ErrorCode.RE_NOT_FOUND})
                except Exception as ex:
                    logger.exception(ex)

            except ApiError as ex:
                try:
                    logger.exception(ex)
                    _is_error = True
                    _serializer_data = {'code': ex.code} if ex.message is None else {
                        'code': ex.code,
                        'message': ex.message
                    }
                    _status = map_error_code_to_http_status(ex.code)
                    _error = ErrorSerializer(_serializer_data)
                except Exception as ex:
                    logger.exception(ex)

            except Exception as ex:
                logger.exception(ex)
                _is_error = True

            finally:
                if _is_error:
                    if _status is not None and _error is not None:
                        return Response(_error.data, status=_status)

                    if _status is None and _error is not None:
                        logger.warn(f'No HTTP status for _error={_error}, returning generic error.')
                        _status = status.HTTP_500_INTERNAL_SERVER_ERROR
                        return Response(_error.data, status=_status)

                    if _status is not None and _error is None:
                        logger.warn(f'Cannot obtain serializer but HTTP status is {_status}, returning generic error')
                        _status = status.HTTP_500_INTERNAL_SERVER_ERROR
                        _error = ErrorSerializer({
                            'code': ErrorCode.GE_INTERNAL,
                            'message': 'Internal error, see server logs.',
                        })
                        return Response(_error.data, status=_status)

                    if _status is None and _error is None:
                        logger.warn(f'Returning generic error')
                        _status = status.HTTP_500_INTERNAL_SERVER_ERROR
                        _error = ErrorSerializer({
                            'code': ErrorCode.GE_INTERNAL,
                            'message': 'Internal error, see server logs.',
                        })
                        return Response(_error.data, status=_status)

        return _wrapped_view_func

    return decorator


def validate_request(serializer_class):

    def decorator(view_func):

        # noinspection PyShadowingNames
        @wraps(view_func)
        def _wrapped_view_func(self, request, *args, **kwargs):
            # self: instance of the class with the decorated method
            serialized_request = serializer_class(data=request.data)
            if serialized_request.is_valid():
                return view_func(self, request, serialized_request, *args, **kwargs)
            else:
                error = ErrorSerializer({
                    'code': ErrorCode.GE_BAD_REQUEST,
                    'message': str(serialized_request.errors)
                })
                return Response(error.data, status=status.HTTP_400_BAD_REQUEST)

        return _wrapped_view_func

    return decorator
