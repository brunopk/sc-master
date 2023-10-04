from rest_framework.views import APIView
from rest_framework.response import Response
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from dataclasses import asdict
from sc_master.utils.decorators import catch_errors
from sc_master.serializers.error import Error as ErrorSerializer
from commands.serializers.common.command_result import CommandResult as CommandResultSerializer
from commands.controllers import DeviceController


class Reset(APIView):

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
    def patch(self, _):
        result = DeviceController.reset()
        response = ResponseSerializer(data=asdict(result.data))
        response.is_valid(raise_exception=True)
        return Response(response.data, status=status.HTTP_200_OK)
