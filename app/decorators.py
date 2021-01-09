from functools import wraps
from rest_framework import status
from rest_framework.response import Response
from rest_framework.validators import ValidationError
from rest_framework.exceptions import ParseError
from django.http.response import Http404
from django.db.utils import IntegrityError
from logging import getLogger
from app.serializers.generic.resp_error import RespError
from app.enums import Error
from app.models.scp import ApiError as ScpApiError


def catch_errors():

    logger = getLogger('catch_errors')

    def decorator(view_func):

        # ser error on SCP class

        # noinspection PyBroadException
        @wraps(view_func)
        def _wrapped_view_func(self, request, *args, **kwargs):
            _status = None
            _error = None
            # self: instance of the class with the decorated method
            try:
                return view_func(self, request, *args, **kwargs)
            # it's raised for instance when violating model attribute unique constraint
            except IntegrityError as ex:
                logger.exception(ex)
                _status = status.HTTP_409_CONFLICT
                _error = RespError({
                    'code': int(Error.CANNOT_CREATE_ELEMENT),
                    'message': str(Error.CANNOT_CREATE_ELEMENT),
                    'description': str(ex)
                })
            except ParseError as ex:
                logger.exception(ex)
                _status = status.HTTP_400_BAD_REQUEST
                _error = RespError({
                    'code': int(Error.PARSE_ERROR),
                    'message': str(Error.PARSE_ERROR),
                    'description': str(ex)
                })
            except Http404 as ex:
                logger.exception(ex)
                _status = status.HTTP_400_BAD_REQUEST
                _error = RespError({
                    'code': int(Error.RESOURCE_NOT_FOUND),
                    'message': str(Error.RESOURCE_NOT_FOUND),
                    'description': str(ex)
                })
            # TODO diferentiate errors (for instance in [{'id': [ErrorDetail(string='section with this id already exists.', code='unique')], 'color_hex': [ErrorDetail(string='Invalid pk "string" - object does not exist.', code='does_not_exist')]}])
            except ValidationError as ex:
                logger.exception(ex)
                _status = status.HTTP_400_BAD_REQUEST
                _error = RespError({
                    'code': int(Error.BAD_REQUEST),
                    'message': str(Error.BAD_REQUEST),
                    'description': str(ex)
                })
            except ScpApiError as ex:
                logger.exception(ex)
                _status = ex.status
                _error = RespError({
                    'code': int(Error.SCRPI_SERVICE_ERROR),
                    'message': str(Error.SCRPI_SERVICE_ERROR),
                    'description': f'{ex.message}: {ex.result}'
                })
            except BrokenPipeError as ex:
                logger.exception(ex)
                _status = status.HTTP_503_SERVICE_UNAVAILABLE
                _error = RespError({
                    'code': Error.SCRPI_CONNECTION_ERROR,
                    'message': str(Error.SCRPI_CONNECTION_ERROR),
                    'description': 'See server logs'
                })
            except ConnectionResetError as ex:
                logger.exception(ex)
                _status = status.HTTP_503_SERVICE_UNAVAILABLE
                _error = RespError({
                    'code': Error.SCRPI_CONNECTION_ERROR,
                    'message': str(Error.SCRPI_CONNECTION_ERROR),
                    'description': 'See server logs'
                })
            except Exception as ex:
                logger.exception(ex)
                _status = status.HTTP_500_INTERNAL_SERVER_ERROR
                _error = RespError({
                    'code': Error.INTERNAL_SERVER_ERROR,
                    'message': str(Error.INTERNAL_SERVER_ERROR),
                    'description': 'See server logs'
                })
            finally:
                if _status is not None and _error is not None:
                    return Response(_error.data, status=_status)
        return _wrapped_view_func

    return decorator


def serializer(serializer_class):

    def decorator(view_func):

        # noinspection PyShadowingNames
        @wraps(view_func)
        def _wrapped_view_func(self, request, *args, **kwargs):
            # self: instance of the class with the decorated method
            serialized_request = serializer_class(data=request.data)
            if serialized_request.is_valid():
                return view_func(self, request, serialized_request, *args, **kwargs)
            else:
                error = RespError({
                    'code': int(Error.BAD_REQUEST),
                    'message': str(Error.BAD_REQUEST),
                    'description': str(serialized_request.errors)
                })
                return Response(error.data, status=status.HTTP_400_BAD_REQUEST)

        return _wrapped_view_func

    return decorator
