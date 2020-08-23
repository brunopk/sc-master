from django.db.models import Q
from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.response import Response
from app import serializers, models, constants
from project import settings
from drf_yasg.utils import swagger_auto_schema
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope
from oauth2_provider.models import AccessToken, Application, RefreshToken
from oauthlib import common
from django.utils import timezone
from datetime import timedelta


class Effect(APIView):
    serializer_class = serializers.Effect
    permission_classes = [TokenHasReadWriteScope]

    @swagger_auto_schema(responses={status.HTTP_200_OK: serializers.Effect(many=True)})
    def get(self, request):
        effects = models.Effect.objects.all()
        serializer = serializers.Effect(effects, many=True)
        return Response(serializer.data)


class GetToken(APIView):
    permission_classes = (permissions.AllowAny,)

    @swagger_auto_schema(responses={status.HTTP_200_OK: serializers.GetTokenRequest(),
                                    status.HTTP_400_BAD_REQUEST: serializers.ErrorResponse()},
                         request_body=serializers.GetTokenRequest)
    def post(self, request):
        request.data['grant_type'] = 'password'
        serializedRequest = serializers.GetTokenRequest(data=request.data)
        if serializedRequest.is_valid():
            try:
                user = models.User.objects.get(username=serializedRequest.data.get('username'))
                application = Application.objects.get(client_id=settings.CLIENT_ID)
                query = Q(user=user) & Q(expires__gte=timezone.now())
                access_tokens = AccessToken.objects.filter(query).order_by('-expires')
                for a in access_tokens:
                    a.revoke()
                expires = timezone.now() + timedelta(seconds=settings.ACCESS_TOKEN_EXPIRE_SECONDS)
                token1 = common.generate_token()
                token2 = common.generate_token()
                access_token = AccessToken(
                    user=user,
                    scope=settings.TOKEN_SCOPE,
                    expires=expires,
                    token=token1,
                    application=application
                )
                access_token.save()
                refresh_token = RefreshToken(
                    user=user,
                    token=token2,
                    application=application,
                    access_token=access_token
                )
                refresh_token.save()
                serializedResponse = serializers.GetTokenResponse(data={
                    'token': token1,
                    'refresh_token': token2
                })
                serializedResponse.is_valid(raise_exception=True)
                return Response(serializedResponse.data, status=status.HTTP_200_OK)
            except Exception as e:
                error = serializers.ErrorResponse({
                    'code': constants.ERROR_BAD_REQUEST_CODE,
                    'message': constants.ERROR_BAD_REQUEST_MSG,
                    'description': e.__str__()
                })
                return Response(error.data, status=status.HTTP_400_BAD_REQUEST)

        error = serializers.ErrorResponse({'code': constants.ERROR_BAD_REQUEST_CODE,
                                           'message': constants.ERROR_BAD_REQUEST_MSG,
                                           'description': serializedRequest.errors.__str__()})
        return Response(error.data, status=status.HTTP_400_BAD_REQUEST)
