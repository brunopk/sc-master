from rest_framework.views import APIView
from rest_framework.response import Response
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from dataclasses import asdict
from sc_master.controllers.device_controller import DeviceController
from sc_master.utils.decorators import catch_errors
from commands.serializers.common.response import Response as ResponseSerializer


class TurnOff(APIView):

    permission_classes = [TokenHasReadWriteScope]

    required_scopes = ['commands']

    # noinspection PyShadowingBuiltins
    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: ResponseSerializer(),
            status.HTTP_404_NOT_FOUND: ResponseSerializer(),
            status.HTTP_500_INTERNAL_SERVER_ERROR: ResponseSerializer(),
            status.HTTP_503_SERVICE_UNAVAILABLE: ResponseSerializer(),
        }
    )
    @catch_errors()
    def patch(self, _, index=None):
        result = DeviceController.turn_on(index)
        response = ResponseSerializer(data=asdict(result))
        response.is_valid(raise_exception=True)
        return Response(response.data, status=result.http_status)
