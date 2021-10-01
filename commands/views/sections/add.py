from rest_framework.views import APIView
from rest_framework.response import Response
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from dataclasses import asdict
from sc_master.controllers.device_controller import DeviceController
from sc_master.utils.decorators import catch_errors, validate_request
from sc_master.utils.helpers import map_sections
from commands.serializers.common.response import Response as ResponseSerializer
from commands.serializers.sections.add import Add as AddSectionSerializer


class Add(APIView):

    permission_classes = [TokenHasReadWriteScope]

    required_scopes = ['commands']

    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: ResponseSerializer(),
            status.HTTP_409_CONFLICT: ResponseSerializer(),
            status.HTTP_400_BAD_REQUEST: ResponseSerializer(),
            status.HTTP_404_NOT_FOUND: ResponseSerializer(),
            status.HTTP_500_INTERNAL_SERVER_ERROR: ResponseSerializer,
            status.HTTP_503_SERVICE_UNAVAILABLE: ResponseSerializer()
        },
        request_body=AddSectionSerializer,
    )
    @catch_errors()
    @validate_request(serializer_class=AddSectionSerializer)
    def put(self, _, serialized_request):
        result = DeviceController.add_sections(map_sections(serialized_request.data.get('sections')))
        response = ResponseSerializer(data=asdict(result.data))
        response.is_valid(raise_exception=True)
        return Response(response.data, status=result.http_status)
