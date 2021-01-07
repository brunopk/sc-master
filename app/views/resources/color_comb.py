from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.serializers import ListSerializer
from app.decorators import catch_errors
from app.models import ColorCombination
from app.serializers.resources.color_comb import ResrColorCombination as ResrColorCombinationSerializer
from app.serializers.generic.resp_error import RespError
from app.serializers.generic.resp_ok import RespOk
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope
from drf_yasg.utils import swagger_auto_schema


class ResrColorCombination(ModelViewSet):
    serializer_class = ResrColorCombinationSerializer
    queryset = ColorCombination.objects.all()
    permission_classes = [TokenHasReadWriteScope]
    http_method_names = ['post', 'get', 'delete']

    @swagger_auto_schema(
        responses={
            status.HTTP_500_INTERNAL_SERVER_ERROR: RespError,
            status.HTTP_400_BAD_REQUEST: RespError(),
            status.HTTP_409_CONFLICT: RespError(),
            status.HTTP_201_CREATED: ResrColorCombinationSerializer()
        },
        request_body=ResrColorCombinationSerializer,
    )
    @catch_errors()
    def create(self, request, *args, **kwargs):
        return super(ResrColorCombination, self).create(request, *args, **kwargs)

    @swagger_auto_schema(
        responses={
            status.HTTP_500_INTERNAL_SERVER_ERROR: RespError(),
            status.HTTP_404_NOT_FOUND: RespError(),
            status.HTTP_204_NO_CONTENT: RespOk()
        }
    )
    @catch_errors()
    def destroy(self, request, *args, **kwargs):
        return super(ResrColorCombination, self).destroy(request, *args, **kwargs)

    # noinspection PyShadowingNames
    @swagger_auto_schema(
        responses={
            status.HTTP_500_INTERNAL_SERVER_ERROR: RespError(),
            status.HTTP_200_OK: ListSerializer(child=ResrColorCombinationSerializer())
        }
    )
    @catch_errors()
    def list(self, request, *args, **kwargs):
        return super(ResrColorCombination, self).list(request, *args, **kwargs)

    @swagger_auto_schema(
        responses={
            status.HTTP_500_INTERNAL_SERVER_ERROR: RespError(),
            status.HTTP_404_NOT_FOUND: RespError(),
            status.HTTP_200_OK: ResrColorCombinationSerializer()
        }
    )
    @catch_errors()
    def retrieve(self, request, *args, **kwargs):
        return super(ResrColorCombination, self).retrieve(request, *args, **kwargs)
