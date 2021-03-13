from rest_framework.views import APIView
from rest_framework.response import Response
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.exceptions import ValidationError
from app.serializers.generic.resp_error import RespError
from app.serializers.generic.resp_ok import RespOk
from app.decorators import catch_errors
from app.models import Section, scrpi_client
from app.enums import Error


class CmdTurnOffSection(APIView):

    permission_classes = [TokenHasReadWriteScope]

    # noinspection PyShadowingBuiltins
    @swagger_auto_schema(
        responses={
            status.HTTP_500_INTERNAL_SERVER_ERROR: RespError,
            status.HTTP_503_SERVICE_UNAVAILABLE: RespError(),
            status.HTTP_404_NOT_FOUND: RespError(),
            status.HTTP_400_BAD_REQUEST: RespError(),
            status.HTTP_200_OK: RespOk}
    )
    @catch_errors()
    def patch(self, _, pk=None):
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
                if section.is_on:
                    scrpi_client.set_color(f'#000000', section.sc_rpi_id)
                    section.is_on = False
                    section.save()
                    return Response({}, status=status.HTTP_200_OK)
                else:
                    resp = RespError(data={
                        'code': int(Error.SECTION_IS_ALREADY_OFF),
                        'message': str(Error.SECTION_IS_ALREADY_OFF),
                        'description': f'section {pk} is off'
                    })
                    resp.is_valid(raise_exception=True)
                    return Response(resp.data, status=status.HTTP_400_BAD_REQUEST)
        except ValidationError:
            raise Exception()

