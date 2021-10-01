from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.serializers import ListSerializer
from drf_yasg.utils import swagger_auto_schema
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope
from sc_master.utils.decorators import catch_errors
from sc_master.serializers.error import Error as ErrorSerializer
from resources.models import Color
from resources.serializers.color import Color as ColorSerializer


class Color(ModelViewSet):

    serializer_class = ColorSerializer

    queryset = Color.objects.all()

    lookup_field = 'id'

    permission_classes = [TokenHasReadWriteScope]

    required_scopes = 'resources'

    http_method_names = ['post', 'get', 'delete']

    @swagger_auto_schema(
        responses={
            status.HTTP_500_INTERNAL_SERVER_ERROR: ErrorSerializer(),
            status.HTTP_400_BAD_REQUEST: ErrorSerializer(),
            status.HTTP_409_CONFLICT: ErrorSerializer(),
            status.HTTP_201_CREATED: ColorSerializer()
        },
        request_body=ColorSerializer,
    )
    @catch_errors()
    def create(self, request, *args, **kwargs):
        return super(Color, self).create(request, *args, **kwargs)

    @swagger_auto_schema(
        responses={
            status.HTTP_204_NO_CONTENT: None,
            status.HTTP_404_NOT_FOUND: ErrorSerializer(),
            status.HTTP_500_INTERNAL_SERVER_ERROR: ErrorSerializer(),

        }
    )
    @catch_errors()
    def destroy(self, request, *args, **kwargs):
        return super(Color, self).destroy(request, *args, **kwargs)

    # noinspection PyShadowingNames
    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: ListSerializer(child=ColorSerializer()),
            status.HTTP_500_INTERNAL_SERVER_ERROR: ErrorSerializer()
        }
    )
    @catch_errors()
    def list(self, request, *args, **kwargs):
        return super(Color, self).list(request, *args, **kwargs)

    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: ColorSerializer(),
            status.HTTP_404_NOT_FOUND: ErrorSerializer(),
            status.HTTP_500_INTERNAL_SERVER_ERROR: ErrorSerializer(),
        }
    )
    @catch_errors()
    def retrieve(self, request, *args, **kwargs):
        return super(Color, self).retrieve(request, *args, **kwargs)
