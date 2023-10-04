from rest_framework.views import APIView
from rest_framework.response import Response
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from dataclasses import asdict
from sc_master.utils.decorators import catch_errors
from sc_master.serializers.error import Error as ErrorSerializer
from commands.serializers.common.response import Response as ResponseSerializer
from commands.controllers import DeviceController


class TurnOn(APIView):

    permission_classes = [TokenHasReadWriteScope]

    required_scopes = ['commands']

    # noinspection PyBroadException
    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: ResponseSerializer(),
            status.HTTP_500_INTERNAL_SERVER_ERROR: ErrorSerializer(),
            status.HTTP_503_SERVICE_UNAVAILABLE: ErrorSerializer(),
        }
    )
    @catch_errors()
    def patch(self, _, ):
        result = DeviceController.turn_on()
        response = ResponseSerializer(data=asdict(result))
        response.is_valid(raise_exception=True)
        return Response(response.data, status=status.HTTP_200_OK)
