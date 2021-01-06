from functools import wraps
from rest_framework import status
from rest_framework.response import Response
from rest_framework.validators import ValidationError
from django.http.response import Http404
from logging import getLogger
from app.serializers.resp.error import RespError
from app.enums import Error
from app.scp import ApiError as ScpApiError


def catch_errors():

    logger = getLogger('catch_scp_errors')

    def decorator(view_func):

        # ser error on SCP class

        @wraps(view_func)
        def _wrapped_view_func(self, request, *args, **kwargs):
            # self: instance of the class with the decorated method
            try:
                return view_func(self, request, *args, **kwargs)
            except Http404 as ex:
                logger.info('Not found')
                error = RespError({
                    'code': int(Error.RESOURCE_NOT_FOUND),
                    'message': str(Error.RESOURCE_NOT_FOUND),
                    'description': str(ex)
                })
                return Response(error.data, status=status.HTTP_400_BAD_REQUEST)
            except ValidationError as ex:
                logger.info('Bad request')
                error = RespError({
                    'code': int(Error.BAD_REQUEST),
                    'message': str(Error.BAD_REQUEST),
                    'description': str(ex)
                })
                return Response(error.data, status=status.HTTP_400_BAD_REQUEST)
            except ScpApiError as ex:
                logger.warning(f'SCP error {ex.status}: {ex.message}, {str(ex.result)}')
                error = RespError({
                    'code': int(Error.SCDRIVER_SERVICE_ERROR),
                    'message': str(Error.SCDRIVER_SERVICE_ERROR),
                    'description': ex.message
                })
                return Response(error.data, status=ex.status)
            except BrokenPipeError as ex:
                logger.exception(ex)
                error = RespError({
                    'code': Error.SCDRIVER_UNAVAILABLE,
                    'message': str(Error.SCDRIVER_UNAVAILABLE),
                    'description': 'See server logs'
                })
                return Response(error.data, status=status.HTTP_503_SERVICE_UNAVAILABLE)
            except ConnectionResetError as ex:
                logger.exception(ex)
                error = RespError({
                    'code': Error.SCDRIVER_UNAVAILABLE,
                    'message': str(Error.SCDRIVER_UNAVAILABLE),
                    'description': 'See server logs'
                })
                return Response(error.data, status=status.HTTP_503_SERVICE_UNAVAILABLE)
            except Exception as ex:
                logger.exception(ex)
                error = RespError({
                    'code': Error.INTERNAL_SERVER_ERROR,
                    'message': str(Error.INTERNAL_SERVER_ERROR),
                    'description': 'See server logs'
                })
                return Response(error.data, status=status.HTTP_503_SERVICE_UNAVAILABLE)
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
