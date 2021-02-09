from rest_framework.views import APIView
from rest_framework.response import Response
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from app.models import scrpi_client
from app.serializers.generic.resp_ok import RespOk
from app.serializers.generic.resp_error import RespError
from app.decorators import catch_errors


# TODO: there should be a CmdTurnOn View

class CmdTurnOff(APIView):

    permission_classes = [TokenHasReadWriteScope]

    @swagger_auto_schema(
        responses={
            status.HTTP_500_INTERNAL_SERVER_ERROR: RespError,
            status.HTTP_503_SERVICE_UNAVAILABLE: RespError(),
            status.HTTP_200_OK: RespOk()
        }
    )
    @catch_errors()
    def patch(self, _, ):
        # TODO: fix: edited section must be saved when strip is turned off and restored strip is turned on
        scrpi_client.reset()
        scrpi_client.set_color("#000000")
        return Response({}, status=status.HTTP_200_OK)

