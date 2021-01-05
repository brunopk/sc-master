from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from app.decorators import catch_errors
from app.models import Color
from app.serializers.resr_color import ResrColor as ResrColorSerializer
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope


class ResrColor(ModelViewSet):
    serializer_class = ResrColorSerializer
    queryset = Color.objects.all()
    permission_classes = [TokenHasReadWriteScope]
    http_method_names = ['post', 'get', 'delete']

    @catch_errors()
    def create(self, request, *args, **kwargs):
        return super(ResrColor, self).create(request, *args, **kwargs)

    @catch_errors()
    def destroy(self, request, *args, **kwargs):
        return super(ResrColor, self).destroy(request, *args, **kwargs)

    # noinspection PyShadowingNames
    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(Color.objects.all(), many=True)
        return Response(serializer.data)
