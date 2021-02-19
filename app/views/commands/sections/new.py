from rest_framework.views import APIView
from rest_framework.response import Response
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from app.models import scrpi_client
from app.serializers.generic.resp_error import RespError
from app.serializers.commands.sections.new_req import CmdNewSectionReq
from app.serializers.commands.sections.new_resp import CmdNewSectionResp
from app.decorators import catch_errors, serializer


class CmdNewSection(APIView):

    permission_classes = [TokenHasReadWriteScope]

    @swagger_auto_schema(
        responses={
            status.HTTP_500_INTERNAL_SERVER_ERROR: RespError,
            status.HTTP_503_SERVICE_UNAVAILABLE: RespError(),
            status.HTTP_409_CONFLICT: RespError(),
            status.HTTP_400_BAD_REQUEST: RespError(),
            status.HTTP_200_OK: CmdNewSectionResp()},
        request_body=CmdNewSectionReq,
    )
    @catch_errors()
    @serializer(serializer_class=CmdNewSectionReq)
    def patch(self, _, serialized_request):
        start = serialized_request.data.get('start')
        end = serialized_request.data.get('end')
        result = scrpi_client.new_section(start, end)
        return Response({'id': result.get('id')}, status=status.HTTP_200_OK)

