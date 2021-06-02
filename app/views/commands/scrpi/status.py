import traceback
from rest_framework.views import APIView
from rest_framework.response import Response
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from logging import getLogger
from app.models import scrpi_client
from app.serializers.commands.scrpi.status_resp import CmdScRpiStatusResp
from app.serializers.generic.resp_error import RespError
from app.models import NotConnected as ScRpiNotConnected
from app.decorators import catch_errors
from app.enums import Error, ScRpiStatus


# TODO: change CmdScRpiStatusResp adding new data from ApiClient

class CmdScRpiStatus(APIView):

    permission_classes = [TokenHasReadWriteScope]

    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: CmdScRpiStatusResp(),
            status.HTTP_500_INTERNAL_SERVER_ERROR: RespError()
        }
    )
    @catch_errors()
    def patch(self, _):
        try:
            scrpi_resp = scrpi_client.status()
            resp = CmdScRpiStatusResp(data={
                'number_of_led': scrpi_resp.get('number_of_led'),
                'status': ScRpiStatus.OK.__str__(),
            })
            resp.is_valid(raise_exception=True)
            return Response(resp.data, status=status.HTTP_200_OK)
        except Exception as ex:
            if not (
                    isinstance(ex, BrokenPipeError) or
                    isinstance(ex, ConnectionResetError) or
                    isinstance(ex, ScRpiNotConnected)
            ):
                logger = getLogger('CmdScRpiStatus')
                logger.warning(traceback.format_exc())
                resp = RespError(data={
                    'code': Error.INTERNAL_SERVER_ERROR.__int__(),
                    'message': Error.INTERNAL_SERVER_ERROR.__str__(),
                    'description': Error.INTERNAL_SERVER_ERROR.__str__()
                })
                resp.is_valid(raise_exception=True)
                return Response(data=resp.data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            elif isinstance(ex, ScRpiNotConnected):
                resp = CmdScRpiStatusResp(data={'status': ScRpiStatus.NOT_CONNECTED.__str__()})
                resp.is_valid(raise_exception=True)
                return Response(resp.data, status=status.HTTP_200_OK)
            resp = CmdScRpiStatusResp(data={
                'status': ScRpiStatus.HAS_ERROR.__str__(),
                'status_details': ex.__class__.__name__
            })
            resp.is_valid(raise_exception=True)
            return Response(resp.data, status=status.HTTP_200_OK)
