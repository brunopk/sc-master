from rest_framework.views import APIView
from rest_framework.response import Response
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from dataclasses import asdict
from sc_master.serializers.error import Error as ErrorSerializer
from sc_master.utils.decorators import catch_errors, validate_request
from sc_master.utils.dataclasses import Section
from commands.serializers.common import CommandResult as CommandResultSerializer
from commands.serializers.sections.add import Add as AddSectionSerializer
from commands.controllers import DeviceController


class Add(APIView):

    permission_classes = [TokenHasReadWriteScope]

    required_scopes = ['commands']

    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: CommandResultSerializer(),
            status.HTTP_409_CONFLICT: ErrorSerializer(),
            status.HTTP_400_BAD_REQUEST: ErrorSerializer(),
            status.HTTP_404_NOT_FOUND: ErrorSerializer(),
            status.HTTP_500_INTERNAL_SERVER_ERROR: ErrorSerializer,
            status.HTTP_503_SERVICE_UNAVAILABLE: ErrorSerializer()
        },
        request_body=AddSectionSerializer,
    )
    @catch_errors()
    @validate_request(serializer_class=AddSectionSerializer)
    def put(self, _, serialized_request):
        sections_to_add = serialized_request.validated_data.get('sections')
        sections_to_add = list(map(lambda s: Section(
            s.get('start'), s.get('end'), s.get('color'), False), sections_to_add))
        result = DeviceController.add_sections(sections_to_add)
        return Response(result.data, status=status.HTTP_200_OK)
