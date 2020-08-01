from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response
from app import serializers, models
from drf_yasg.utils import swagger_auto_schema


class Effect(APIView):
    """
    """
    serializer_class = serializers.Effect
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(responses={200: serializers.Effect(many=True)})
    def get(self, request):
        effects = models.Effect.objects.all()
        serializer = serializers.Effect(effects, many=True)
        return Response(serializer.data)
