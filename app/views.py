from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.response import Response
from app import serializers, models, constants
from drf_yasg.utils import swagger_auto_schema
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope


class Effect(APIView):
    serializer_class = serializers.Effect
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]

    @swagger_auto_schema(responses={status.HTTP_200_OK: serializers.Effect(many=True)})
    def get(self, request):
        effects = models.Effect.objects.all()
        serializer = serializers.Effect(effects, many=True)
        return Response(serializer.data)


#class Token(APIView):
#    serializer_class = serializers.LoginDataRequest

#    @swagger_auto_schema(responses={status.HTTP_200_OK: serializers.LoginDataResponse(),
#                                    status.HTTP_400_BAD_REQUEST: serializers.ErrorResponse()},
#                         request_body=serializers.LoginDataRequest)
#    def post(self, request, format=None):
#        loginData = serializers.LoginDataResponse(data=request.data)
#        if loginData.is_valid():
#            return Response(loginData.data, status=status.HTTP_200_OK)
#        error = serializers.ErrorResponse({'code': constants.ERROR_BAD_REQUEST_CODE,
#                                           'message': constants.ERROR_BAD_REQUEST_MSG,
#                                           'description': loginData.errors.__str__()})
#        return Response(error.data, status=status.HTTP_400_BAD_REQUEST)
