from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.serializers import ListSerializer
from app.decorators import catch_errors
from app.models import Color
from app.serializers.resr.color import ResrColor as ResrColorSerializer
from app.serializers.resp.error import RespError
from app.serializers.resp.ok import RespOk
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope
from drf_yasg.utils import swagger_auto_schema


class ResrColor(ModelViewSet):
    serializer_class = ResrColorSerializer
    queryset = Color.objects.all()
    lookup_field = 'hex'
    permission_classes = [TokenHasReadWriteScope]
    http_method_names = ['post', 'get', 'delete']

    @swagger_auto_schema(
        responses={
            status.HTTP_500_INTERNAL_SERVER_ERROR: RespError,
            status.HTTP_400_BAD_REQUEST: RespError(),
            status.HTTP_409_CONFLICT: RespError(),
            status.HTTP_201_CREATED: ResrColorSerializer()
        },
        request_body=ResrColorSerializer,
    )
    @catch_errors()
    def create(self, request, *args, **kwargs):
        return super(ResrColor, self).create(request, *args, **kwargs)

    @swagger_auto_schema(
        responses={
            status.HTTP_500_INTERNAL_SERVER_ERROR: RespError(),
            status.HTTP_404_NOT_FOUND: RespError(),
            status.HTTP_204_NO_CONTENT: RespOk()
        }
    )
    @catch_errors()
    def destroy(self, request, *args, **kwargs):
        return super(ResrColor, self).destroy(request, *args, **kwargs)

    # noinspection PyShadowingNames
    @swagger_auto_schema(
        responses={
            status.HTTP_500_INTERNAL_SERVER_ERROR: RespError(),
            status.HTTP_200_OK: ListSerializer(child=ResrColorSerializer())
        }
    )
    @catch_errors()
    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(Color.objects.all(), many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        responses={
            status.HTTP_500_INTERNAL_SERVER_ERROR: RespError(),
            status.HTTP_404_NOT_FOUND: RespError(),
            status.HTTP_200_OK: ResrColorSerializer()
        }
    )
    @catch_errors()
    def retrieve(self, request, *args, **kwargs):
        return super(ResrColor, self).retrieve(request, *args, **kwargs)
