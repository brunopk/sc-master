from rest_framework.views import APIView
from rest_framework.response import Response
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.exceptions import ValidationError
from app.models import scrpi_client, Section, Color
from app.serializers.generic.resp_error import RespError
from app.serializers.generic.resp_ok import RespOk
from app.serializers.commands.sections.edit_req import CmdEditSectionReq
from app.decorators import catch_errors, serializer
from app.enums import Error


class CmdEditSection(APIView):

    permission_classes = [TokenHasReadWriteScope]

    # noinspection PyShadowingBuiltins
    @swagger_auto_schema(
        responses={
            status.HTTP_500_INTERNAL_SERVER_ERROR: RespError,
            status.HTTP_503_SERVICE_UNAVAILABLE: RespError(),
            status.HTTP_400_BAD_REQUEST: RespError(),
            status.HTTP_404_NOT_FOUND: RespError(),
            status.HTTP_200_OK: RespOk},
        request_body=CmdEditSectionReq,
    )
    @catch_errors()
    @serializer(serializer_class=CmdEditSectionReq)
    def patch(self, _, serialized_request, pk):
        section = Section.objects.get(id=pk)
        try:
            if not section.static_design.active:
                resp = RespError(data={
                    'code': int(Error.SECTION_NOT_IN_ACTIVE_STATIC_DESIGN),
                    'message': str(Error.SECTION_NOT_IN_ACTIVE_STATIC_DESIGN),
                    'description': f'section {pk} is not included in the current static design'
                })
                resp.is_valid(raise_exception=True)
                return Response(resp.data, status=status.HTTP_400_BAD_REQUEST)
            else:
                hw_section_id = section.hw_id
                start = serialized_request.data.get('start')
                end = serialized_request.data.get('end')
                color = Color.objects.get(pk=serialized_request.data.get('color'))
                scrpi_client.section_edit(hw_section_id.__str__(), start=start, end=end, color=color.hex)
                return Response({}, status=status.HTTP_200_OK)
        except ValidationError:
            raise Exception()

