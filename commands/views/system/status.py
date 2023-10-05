from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope
from drf_yasg.utils import swagger_auto_schema
from dataclasses import asdict
from commands.serializers.common import CommandResult as CommandResultSerializer
from commands.controllers import DeviceController
from sc_master.serializers.error import Error as ErrorSerializer
from sc_master.utils.decorators import catch_errors


class Status(APIView):

    permission_classes = [TokenHasReadWriteScope]

    required_scopes = ['commands']

    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: CommandResultSerializer(),
            status.HTTP_500_INTERNAL_SERVER_ERROR: ErrorSerializer(),
            status.HTTP_503_SERVICE_UNAVAILABLE: ErrorSerializer()
        }
    )
    @catch_errors()
    def get(self, _):
        result = DeviceController.status()
        return Response(result.data, status=status.HTTP_200_OK)
