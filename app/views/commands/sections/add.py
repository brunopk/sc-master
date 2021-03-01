from rest_framework.views import APIView
from rest_framework.response import Response
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from app.serializers.generic.resp_error import RespError
from app.serializers.commands.sections.add_resp import CmdAddSectionResp
from app.serializers.commands.sections.add_req import CmdAddSectionReq
from app.serializers.commands.sections.section_resp import SectionResp
from app.decorators import catch_errors, serializer
from app.models import StaticDesign, Section, Color, scrpi_client
from app.enums import Error

# TODO: try combining CmdAddSectionResp and CmdAddSectionReq in one


# noinspection PyShadowingBuiltins
def merge_sort(list):
    if len(list) > 1:
        result = []
        m = len(list) // 2
        l1 = list[:m]
        l2 = list[m:]
        l1 = merge_sort(l1)
        l2 = merge_sort(l2)
        i = 0
        j = 0
        while i < len(l1) and j < len(l2):
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


class Overlapping(Exception):
    pass


class CmdAddSection(APIView):

    permission_classes = [TokenHasReadWriteScope]

    # noinspection PyShadowingBuiltins,PyBroadException,PyUnresolvedReferences
    @swagger_auto_schema(
        responses={
            status.HTTP_500_INTERNAL_SERVER_ERROR: RespError,
            status.HTTP_503_SERVICE_UNAVAILABLE: RespError(),
            status.HTTP_409_CONFLICT: RespError(),
            status.HTTP_400_BAD_REQUEST: RespError(),
            status.HTTP_404_NOT_FOUND: RespError(),
            status.HTTP_200_OK: CmdAddSectionResp},
        request_body=CmdAddSectionReq,
    )
    @catch_errors()
    @serializer(serializer_class=CmdAddSectionReq)
    def patch(self, _, serialized_request):

        new_static_design_created = False

        try:
            static_design = StaticDesign.objects.get(active=True)
        except StaticDesign.DoesNotExist:
            static_design = StaticDesign(active=True)
            static_design.save()
            new_static_design_created = True

        new_sections = serialized_request.data.get('sections')
        l1 = [(x.start, x.end) for x in static_design.section_set.all()]
        l2 = [(x.get('start'), x.get('end')) for x in new_sections]

        try:
            # raise exception if detects overlapping
            merge_sort(l1 + l2)
            aux = [(x.get('start'), x.get('end'), Color.objects.get(pk=x.get('color'))) for x in new_sections]
            new_sections = []
            i = 0
            for x in aux:
                x = Section(start=x[0], end=x[1], color=x[2], static_design=static_design)
                sc_rpi_result = scrpi_client.new_section(x.start, x.end)
                sc_rpi_id = sc_rpi_result.get('id')
                scrpi_client.set_color(x.color.hex, sc_rpi_id)
                x.sc_rpi_id = sc_rpi_id
                x.save()
                new_sections.append(x)
            try:
                result_sections = []
                for x in new_sections:
                    x = SectionResp(data={
                        'id': x.id,
                        'start': x.start,
                        'end': x.end,
                        'color': x.color.id
                    })
                    x.is_valid(raise_exception=True)
                    result_sections.append(x.data)
                result = CmdAddSectionResp(data={'sections': result_sections})
                result.is_valid(raise_exception=True)
            except Exception:
                raise Exception()
            return Response(result.data, status=status.HTTP_200_OK)
        except Overlapping:
            if new_static_design_created:
                static_design.delete()
            error = RespError({
                'code': Error.SECTION_OVERLAPPING,
                'message': str(Error.SECTION_OVERLAPPING),
                'description': str(Error.SECTION_OVERLAPPING)
            })
            return Response(error.data, status=status.HTTP_409_CONFLICT)
        except Exception as ex:
            # should be better with an automatic rollback (google drf transactions)
            for x in new_sections:
                if isinstance(x, Section):
                    x.delete()
            if new_static_design_created:
                static_design.delete()
            raise ex
