from rest_framework.views import APIView
from rest_framework.response import Response
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from app.serializers.generic.resp_error import RespError
from app.serializers.generic.resp_ok import RespOk
from app.decorators import catch_errors
from app.models import Section, scrpi_client


class CmdTurnOnSection(APIView):

    permission_classes = [TokenHasReadWriteScope]

    # noinspection PyShadowingBuiltins
    @swagger_auto_schema(
        responses={
            status.HTTP_500_INTERNAL_SERVER_ERROR: RespError,
            status.HTTP_503_SERVICE_UNAVAILABLE: RespError(),
            status.HTTP_404_NOT_FOUND: RespError(),
            status.HTTP_200_OK: RespOk}
    )
    @catch_errors()
    def patch(self, _, pk=None):
        section = Section.objects.get(id=pk)

        if section.is_on:
            scrpi_client.set_color('#000000', section.sc_rpi_id)
            section.is_on = False
        else:
            scrpi_client.set_color(f'#{section.color.hex}', section.sc_rpi_id)
            section.is_on = True
        section.save()
        return Response({}, status=status.HTTP_200_OK)

