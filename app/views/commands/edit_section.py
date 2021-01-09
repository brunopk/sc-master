from rest_framework.views import APIView
from rest_framework.response import Response
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from app.models.scp import scp
from app.serializers.generic.resp_error import RespError
from app.serializers.generic.resp_ok import RespOk
from app.serializers.commands.edit_section_req import CmdEditSectionReq
from app.decorators import catch_errors, serializer


class CmdEditSection(APIView):

    permission_classes = [TokenHasReadWriteScope]

    # noinspection PyShadowingBuiltins
    @swagger_auto_schema(
        responses={
            status.HTTP_500_INTERNAL_SERVER_ERROR: RespError,
            status.HTTP_503_SERVICE_UNAVAILABLE: RespError(),
            status.HTTP_400_BAD_REQUEST: RespError(),
            status.HTTP_200_OK: RespOk},
        request_body=CmdEditSectionReq,
    )
    @catch_errors()
    @serializer(serializer_class=CmdEditSectionReq)
    def patch(self, _, serialized_request):
        id = serialized_request.data.get('section_id')
        start = serialized_request.data.get('start')
        end = serialized_request.data.get('end')
        color = serialized_request.data.get('color')
        scp.edit_section(id, start=start, end=end, color=color)
        return Response({}, status=status.HTTP_200_OK)

