from rest_framework.views import APIView
from rest_framework.response import Response
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope
from drf_yasg.utils import swagger_auto_schema
from dataclasses import asdict
from rest_framework import status
from commands.serializers.sections.remove import Remove as RemoveSectionSerializer
from commands.serializers.common.response import Response as ResponseSerializer
from commands.controllers import DeviceController
from sc_master.utils.decorators import catch_errors, validate_request


class Remove(APIView):

    permission_classes = [TokenHasReadWriteScope]

    required_scopes = ['commands']

    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: ResponseSerializer(),
            status.HTTP_404_NOT_FOUND: ResponseSerializer(),
            status.HTTP_500_INTERNAL_SERVER_ERROR: ResponseSerializer(),
            status.HTTP_503_SERVICE_UNAVAILABLE: ResponseSerializer(),
        },
        request_body=RemoveSectionSerializer,
    )
    @catch_errors()
    @validate_request(serializer_class=RemoveSectionSerializer)
    def delete(self, serialized_request):
        result = DeviceController.remove_sections(serialized_request.data)
        response = ResponseSerializer(data=asdict(result.data))
        response.is_valid(raise_exception=True)
        return Response(response.data, result.http_status)
