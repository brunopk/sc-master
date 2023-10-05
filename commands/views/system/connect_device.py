from rest_framework.views import APIView
from rest_framework.response import Response
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from dataclasses import asdict
from sc_master.serializers.error import Error as ErrorSerializer
from sc_master.utils.decorators import catch_errors, validate_request
from commands.serializers.system.connect_device import ConnectDevice as ConnectDeviceSerializer
from commands.serializers.common import CommandResult as CommandResultSerializer
from commands.controllers import DeviceController

# TODO: revisar todos los return code de todos los comandos 

class ConnectDevice(APIView):

    permission_classes = [TokenHasReadWriteScope]

    required_scopes = ['commands']

    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: CommandResultSerializer(),
            status.HTTP_400_BAD_REQUEST: ErrorSerializer(),
            status.HTTP_409_CONFLICT: ErrorSerializer(),
            status.HTTP_500_INTERNAL_SERVER_ERROR: ErrorSerializer(),
            status.HTTP_503_SERVICE_UNAVAILABLE: ErrorSerializer()
        },
        request_body=ConnectDeviceSerializer()
    )
    @catch_errors()
    @validate_request(serializer_class=ConnectDeviceSerializer)
    def put(self, _, serialized_request):
        address = serialized_request.data.get('address')
        port = serialized_request.data.get('port')
        result = DeviceController.connect_device(address, port)
        return Response(result.data, status=status.HTTP_200_OK)
