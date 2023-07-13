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


def catch_errors():

    logger = getLogger('catch_errors')

    def decorator(view_func):

        # noinspection PyBroadException
        @wraps(view_func)
        def _wrapped_view_func(self, request, *args, **kwargs):

            _status = None
            _error = None

            # self is the instance of the class with the decorated method
            try:
                return view_func(self, request, *args, **kwargs)

            except DeviceClientError as ex:
                try:
                    # TODO: SEGUIR: obtener los datos del DeviceClientError (que tipo de error es, puerto, direccion etc)
                    _serializer_data = {'code': ""} 1 is None else {
                        'code': ex.code,
                        'message': ex.message
                    }
                    _status = map_error_code_to_http_status(ex.code)
                    _error = ErrorSerializer(_serializer_data)
                except Exception as ex:
                    logger.exception(ex)
                    _status = status.HTTP_500_INTERNAL_SERVER_ERROR
                    _error = ErrorSerializer({
                        'code': ErrorCode.GE_INTERNAL,
                        'message': 'Internal error, see server logs.',
                    })

            # for instance when violating model attribute unique constraint
            except IntegrityError as ex:
                try:
                    logger.exception(ex)
                    _status = map_error_code_to_http_status(ErrorCode.GE_CANNOT_CREATE_RESOURCE)
                    _error = ErrorSerializer({
                        'code': ErrorCode.GE_CANNOT_CREATE_RESOURCE,
                        'message': f'Cannot create resource {ex}.',
                    })
                except Exception as ex:
                    logger.exception(ex)
                    _status = status.HTTP_500_INTERNAL_SERVER_ERROR
                    _error = ErrorSerializer({
                        'code': ErrorCode.GE_INTERNAL,
                        'message': 'Internal error, see server logs.',
                    })

            except ParseError as ex:
                try:
                    logger.exception(ex)
                    _status = map_error_code_to_http_status(ErrorCode.GE_PARSE_ERROR)
                    _error = ErrorSerializer({
                        'code': ErrorCode.GE_PARSE_ERROR,
                        'message': 'Cannot parse request.',
                    })
                except Exception as ex:
                    logger.exception(ex)
                    _status = status.HTTP_500_INTERNAL_SERVER_ERROR
                    _error = ErrorSerializer({
                        'code': ErrorCode.GE_INTERNAL,
                        'message': 'Internal error, see server logs.',
                    })

            except Http404 as ex:
                try:
                    logger.exception(ex)
                    _status = map_error_code_to_http_status(ErrorCode.RE_NOT_FOUND)
                    _error = ErrorSerializer({
                        'code': ErrorCode.RE_NOT_FOUND,
                        'message': f'Resource not found {ex}.',
                    })
                except Exception as ex:
                    logger.exception(ex)
                    _status = status.HTTP_500_INTERNAL_SERVER_ERROR
                    _error = ErrorSerializer({
                        'code': ErrorCode.GE_INTERNAL,
                        'message': 'Internal error, see server logs.',
                    })

            except ObjectDoesNotExist as ex:
                try:
                    logger.exception(ex)
                    _status = map_error_code_to_http_status(ErrorCode.RE_NOT_FOUND)
                    _error = ErrorSerializer({'code': ErrorCode.RE_NOT_FOUND})
                except Exception as ex:
                    logger.exception(ex)
                    _status = status.HTTP_500_INTERNAL_SERVER_ERROR
                    _error = ErrorSerializer({
                        'code': ErrorCode.GE_INTERNAL,
                        'message': 'Internal error, see server logs.',
                    })
            
            except ApiError as ex:
                try:
                    _serializer_data = {'code': ex.code} if ex.message is None else {
                        'code': ex.code,
                        'message': ex.message
                    }
                    _status = map_error_code_to_http_status(ex.code)
                    _error = ErrorSerializer(_serializer_data)
                except Exception as ex:
                    logger.exception(ex)
                    _status = status.HTTP_500_INTERNAL_SERVER_ERROR
                    _error = ErrorSerializer({
                        'code': ErrorCode.GE_INTERNAL,
                        'message': 'Internal error, see server logs.',
                    })

            except Exception as ex:
                logger.exception(ex)
                _status = status.HTTP_500_INTERNAL_SERVER_ERROR
                _error = ErrorSerializer({
                    'code': ErrorCode.GE_INTERNAL,
                    'message': 'Internal error, see server logs.',
                })

            finally:
                if _status is not None and _error is not None:
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
