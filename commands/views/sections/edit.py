from rest_framework.views import APIView
from rest_framework.response import Response
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from dataclasses import asdict
from sc_master.serializers.error import Error as ErrorSerializer
from sc_master.utils.decorators import catch_errors, validate_request
from sc_master.utils.dataclasses import Section
from commands.serializers.sections.edit import Edit as EditSectionSerializer
from commands.serializers.common import CommandResult as CommandResultSerializer
from commands.controllers import DeviceController


class Edit(APIView):

    permission_classes = [TokenHasReadWriteScope]

    required_scopes = ['commands']

    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: CommandResultSerializer(),
            status.HTTP_400_BAD_REQUEST: ErrorSerializer(),
            status.HTTP_404_NOT_FOUND: ErrorSerializer(),
            status.HTTP_409_CONFLICT: ErrorSerializer(),
            status.HTTP_500_INTERNAL_SERVER_ERROR: ErrorSerializer(),
            status.HTTP_503_SERVICE_UNAVAILABLE: ErrorSerializer(),
        },
        request_body=EditSectionSerializer,
    )
    @catch_errors()
    @validate_request(serializer_class=EditSectionSerializer)
    def patch(self, _, serialized_request, index):
        edited_section = Section(
            serialized_request.data.get('start'),
            serialized_request.data.get('end'),
            serialized_request.data.get('color'),
            None)
        result = DeviceController.edit_section(int(index), edited_section)
        return Response(result.data, status=status.HTTP_200_OK)
