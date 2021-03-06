from rest_framework.views import APIView
from rest_framework.response import Response
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from app.models import scrpi_client
from app.serializers.generic.resp_ok import RespOk
from app.serializers.generic.resp_error import RespError
from app.serializers.commands.set_color_req import CmdSetColorReq
from app.decorators import catch_errors, serializer


class CmdSetColor(APIView):

    permission_classes = [TokenHasReadWriteScope]

    @swagger_auto_schema(
        responses={
            status.HTTP_500_INTERNAL_SERVER_ERROR: RespError,
            status.HTTP_503_SERVICE_UNAVAILABLE: RespError(),
            status.HTTP_409_CONFLICT: RespError(),
            status.HTTP_400_BAD_REQUEST: RespError(),
            status.HTTP_200_OK: RespOk()},
        request_body=CmdSetColorReq,
    )
    @catch_errors()
    @serializer(serializer_class=CmdSetColorReq)
    def patch(self, _, serialized_request):
        section_id = serialized_request.data.get('section_id')
        color = serialized_request.data.get('color')
        scrpi_client.set_color(color, section_id)
        return Response({}, status=status.HTTP_200_OK)

