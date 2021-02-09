from rest_framework.views import APIView
from rest_framework.response import Response
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from app.models import scrpi_client
from app.serializers.commands.connect_scrpi_req import CmdConnectScRpiReq
from app.serializers.commands.connect_scrpi_resp import CmdConnectScRpiResp
from app.serializers.generic.resp_error import RespError
from app.decorators import catch_errors, serializer


# TODO: make scrpi_status endpoint

class CmdConnectScRpi(APIView):

    permission_classes = [TokenHasReadWriteScope]

    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: CmdConnectScRpiResp(),
            status.HTTP_404_NOT_FOUND: RespError(),
            status.HTTP_500_INTERNAL_SERVER_ERROR: RespError(),
            status.HTTP_503_SERVICE_UNAVAILABLE: RespError()
        },
        request_body=CmdConnectScRpiReq()
    )
    @catch_errors()
    @serializer(serializer_class=CmdConnectScRpiReq)
    def patch(self, _, serialized_request):
        scrpi_client.connect(serialized_request.data.get('address'), serialized_request.data.get('port'))
        # TODO: get led_number with scrpi_client (same response fields as scrpi_status)
        return Response({'led_number': 300}, status=status.HTTP_200_OK)

