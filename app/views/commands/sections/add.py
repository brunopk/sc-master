from rest_framework.views import APIView
from rest_framework.response import Response
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope
from drf_yasg.utils import swagger_auto_schema
from django.db import transaction
from rest_framework import status
from app.serializers.generic.resp_error import RespError
from app.serializers.commands.sections.add_resp import CmdAddSectionResp
from app.serializers.commands.sections.add_req import CmdAddSectionReq
from app.serializers.commands.sections.section_resp import SectionResp
from app.decorators import catch_errors, serializer
from app.models import StaticDesign, Section, Color, scrpi_client
from app.enums import Error

# TODO: try combining CmdAddSectionResp and CmdAddSectionReq in one


class CmdAddSection(APIView):

    permission_classes = [TokenHasReadWriteScope]

    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: CmdAddSectionResp(),
            status.HTTP_409_CONFLICT: RespError(),
            status.HTTP_400_BAD_REQUEST: RespError(),
            status.HTTP_404_NOT_FOUND: RespError(),
            status.HTTP_500_INTERNAL_SERVER_ERROR: RespError,
            status.HTTP_503_SERVICE_UNAVAILABLE: RespError()
        },
        request_body=CmdAddSectionReq,
    )
    @catch_errors()
    @serializer(serializer_class=CmdAddSectionReq)
    def patch(self, _, serialized_request):
        try:
            with transaction.atomic():

                # generate StaticDesign (if not exist yet)
                try:
                    static_design = StaticDesign.objects.get(active=True)
                except StaticDesign.DoesNotExist:
                    static_design = StaticDesign(active=True)
                    static_design.save()

                # test overlapping
                new_sections = serialized_request.data.get('sections')
                l1 = [(x.start, x.end) for x in static_design.section_set.all()]
                l2 = [(x.get('start'), x.get('end')) for x in new_sections]
                test_overlapping(l1 + l2)

                # get colors for each section
                colors = [Color.objects.get(pk=s.get('color')) for s in new_sections]

                # generates the corresponding scrpi command args
                command_args = {
                    'sections': [{
                        'start': s.get('start'),
                        'end': s.get('end'),
                        'color': colors[i].hex
                    } for i, s in enumerate(new_sections)]
                }
                command_resp = scrpi_client.section_add(command_args)

                # creates sections in database with the scrpi response data and generates endpoint response
                new_sections_aux = []
                for i, hw_id in enumerate(command_resp.get('sections')):
                    s = Section(
                        start=new_sections[i].get('start'),
                        end=new_sections[i].get('end'),
                        hw_id=hw_id,
                        is_on=True,
                        color=colors[i],
                        static_design=static_design
                    )
                    s.save()
                    s = SectionResp(data={
                        'id': s.id,
                        'start': s.start,
                        'end': s.end,
                        'color': s.color.id
                    })
                    s.is_valid(raise_exception=True)
                    new_sections_aux.append(s.data)
                response = CmdAddSectionResp(data={'sections': new_sections_aux})
                response.is_valid(raise_exception=True)
                return Response(response.data, status=status.HTTP_200_OK)

        except Overlapping:
            error = RespError({
                'code': Error.SECTION_OVERLAPPING,
                'message': str(Error.SECTION_OVERLAPPING),
                'description': str(Error.SECTION_OVERLAPPING)
            })
            return Response(error.data, status=status.HTTP_409_CONFLICT)


class Overlapping(Exception):
    pass


# noinspection PyShadowingBuiltins
def test_overlapping(list):
    """
    Test section overlapping using the merge sort algorithm and in case of detecting any section is overlapping another
    section in the list, raises Overlapping exception.
    """
    if len(list) > 1:
        result = []
        m = len(list) // 2
        l1 = list[:m]
        l2 = list[m:]
        l1 = test_overlapping(l1)
        l2 = test_overlapping(l2)
        i = 0
        j = 0
        while i < len(l1) and j < len(l2):
            # TODO: arreglar esta condicion (ver sc-rpi)
            if l2[j][0] <= l1[i][0] <= l2[j][1] or l2[j][0] <= l1[i][1] <= l2[j][1]:
                raise Overlapping()
            elif l1[i][1] < l2[j][0]:
                result.append(l1[i])
                i += 1
            else:
                result.append(l2[j])
                j += 1
        return result + l1[i:] + l2[j:]
    else:
        return list