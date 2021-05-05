from rest_framework.views import APIView
from rest_framework.response import Response
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope
from drf_yasg.utils import swagger_auto_schema
from django.db import transaction
from rest_framework import status
from app.models import scrpi_client, StaticDesign
from app.serializers.generic.resp_ok import RespOk
from app.serializers.generic.resp_error import RespError
from app.decorators import catch_errors
from app.enums import Error


class CmdTurnOff(APIView):
    """
    Turn off logic must be coherent with turn on logic
    """

    permission_classes = [TokenHasReadWriteScope]

    # noinspection PyBroadException
    @swagger_auto_schema(
        responses={
            status.HTTP_500_INTERNAL_SERVER_ERROR: RespError,
            status.HTTP_503_SERVICE_UNAVAILABLE: RespError(),
            status.HTTP_409_CONFLICT: RespError(),
            status.HTTP_200_OK: RespOk()
        }
    )
    @catch_errors()
    def patch(self, _, ):
        try:
            with transaction.atomic():
                active_static_design = StaticDesign.objects.get(active=True)
                if not active_static_design.is_on:
                    raise SectionIsAlreadyOff()
                else:
                    active_static_design.is_on = True
                    active_static_design.save()
                    scrpi_client.turn_off()
                    return Response({}, status=status.HTTP_200_OK)
        except StaticDesign.DoesNotExist:
            raise Exception()
        except SectionIsAlreadyOff:
            resp = RespError(data={
                'code': int(Error.STRIP_IS_ALREADY_OFF),
                'message': str(Error.STRIP_IS_ALREADY_OFF),
            })
            resp.is_valid(raise_exception=True)
            return Response(resp.data, status=status.HTTP_409_CONFLICT)


class SectionIsAlreadyOff(Exception):
    pass


