from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.serializers import ListSerializer
from app.decorators import catch_errors
from app.models import StaticDesign
from app.serializers.resources.static_design import ResrStaticDesign as ResrStaticDesignSerializer
from app.serializers.generic.resp_error import RespError
from app.serializers.generic.resp_ok import RespOk
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope
from drf_yasg.utils import swagger_auto_schema


class ResrStaticDesign(ModelViewSet):
    serializer_class = ResrStaticDesignSerializer
    queryset = StaticDesign.objects.all()
    permission_classes = [TokenHasReadWriteScope]
    http_method_names = ['post', 'get', 'delete']

    @swagger_auto_schema(
        responses={
            status.HTTP_500_INTERNAL_SERVER_ERROR: RespError,
            status.HTTP_400_BAD_REQUEST: RespError(),
            status.HTTP_409_CONFLICT: RespError(),
            status.HTTP_201_CREATED: ResrStaticDesignSerializer()
        },
        request_body=ResrStaticDesignSerializer,
    )
    @catch_errors()
    def create(self, request, *args, **kwargs):
        return super(ResrStaticDesign, self).create(request, *args, **kwargs)

    @swagger_auto_schema(
        responses={
            status.HTTP_500_INTERNAL_SERVER_ERROR: RespError(),
            status.HTTP_404_NOT_FOUND: RespError(),
            status.HTTP_204_NO_CONTENT: RespOk()
        }
    )
    @catch_errors()
    def destroy(self, request, *args, **kwargs):
        return super(ResrStaticDesign, self).destroy(request, *args, **kwargs)

    # noinspection PyShadowingNames
    @swagger_auto_schema(
        responses={
            status.HTTP_500_INTERNAL_SERVER_ERROR: RespError(),
            status.HTTP_200_OK: ListSerializer(child=ResrStaticDesignSerializer())
        }
    )
    @catch_errors()
    def list(self, request, *args, **kwargs):
        return super(ResrStaticDesign, self).list(request, *args, **kwargs)

    @swagger_auto_schema(
        responses={
            status.HTTP_500_INTERNAL_SERVER_ERROR: RespError(),
            status.HTTP_404_NOT_FOUND: RespError(),
            status.HTTP_200_OK: ResrStaticDesignSerializer()
        }
    )
    @catch_errors()
    def retrieve(self, request, *args, **kwargs):
        return super(ResrStaticDesign, self).retrieve(request, *args, **kwargs)
