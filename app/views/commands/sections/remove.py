from rest_framework.views import APIView
from rest_framework.response import Response
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope
from drf_yasg.utils import swagger_auto_schema
from django.db import transaction
from rest_framework import status
from app.serializers.generic.resp_error import RespError
from app.serializers.generic.resp_ok import RespOk
from app.serializers.commands.sections.remove_req import CmdRemoveSectionsReq
from app.decorators import catch_errors, serializer
from app.models import StaticDesign, scrpi_client
from app.enums import Error


class CmdRemoveSections(APIView):

    permission_classes = [TokenHasReadWriteScope]

    @swagger_auto_schema(
        responses={
            status.HTTP_500_INTERNAL_SERVER_ERROR: RespError,
            status.HTTP_503_SERVICE_UNAVAILABLE: RespError(),
            status.HTTP_404_NOT_FOUND: RespError(),
            status.HTTP_200_OK: RespOk()},
        request_body=CmdRemoveSectionsReq,
    )
    @catch_errors()
    @serializer(serializer_class=CmdRemoveSectionsReq)
    def patch(self, _, serialized_request):
        active_static_design = StaticDesign.objects.get(active=True)
        sections_to_be_removed = active_static_design.section_set.filter(id__in=serialized_request.data.get('sections'))
        if len(sections_to_be_removed) != len(serialized_request.data.get('sections')):
            error = RespError({
                'code': Error.SECTION_NOT_DEFINED_OR_NOT_IN_ACTIVE_STATIC_DESIGN,
                'message': str(Error.SECTION_NOT_DEFINED_OR_NOT_IN_ACTIVE_STATIC_DESIGN),
                'description': str(Error.SECTION_NOT_DEFINED_OR_NOT_IN_ACTIVE_STATIC_DESIGN)
            })
            return Response(error.data, status=status.HTTP_404_NOT_FOUND)
        else:
            with transaction.atomic():
                sections_to_be_removed_aux = [x.hw_id.__str__() for x in sections_to_be_removed]
                sections_to_be_removed.delete()
                scrpi_client.section_remove(sections_to_be_removed_aux)
            return Response({}, status=status.HTTP_200_OK)





