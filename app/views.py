from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.response import Response
from app import serializers
from app.models import scp
from app.decorators import catch_errors, serializer
from app.enums import Error
from project import settings
from drf_yasg.utils import swagger_auto_schema
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope
from oauth2_provider.models import AccessToken, Application, RefreshToken
from oauthlib import common
from django.utils import timezone
from django.contrib.auth import authenticate
from django.db.models import Q
from datetime import timedelta


class SetColor(APIView):

    permission_classes = [TokenHasReadWriteScope]

    @swagger_auto_schema(
        responses={
            status.HTTP_500_INTERNAL_SERVER_ERROR: serializers.RespError,
            status.HTTP_503_SERVICE_UNAVAILABLE: serializers.RespError(),
            status.HTTP_400_BAD_REQUEST: serializers.RespError(),
            status.HTTP_200_OK: serializers.RespOk()},
        request_body=serializers.CmdSetColor
    )
    @catch_errors()
    @serializer(serializer_class=serializers.CmdSetColor)
    def put(self, request, serialized_request):
        section_id = serialized_request.data.get('section_id')
        color = serialized_request.data.get('color')
        scp.set_color(color, section_id)
        return Response({}, status=status.HTTP_200_OK)


class Token(APIView):
    permission_classes = (permissions.AllowAny,)

    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: serializers.ReqToken(),
            status.HTTP_400_BAD_REQUEST: serializers.RespError()},
        request_body=serializers.ReqToken
    )
    @serializer(serializer_class=serializers.ReqToken)
    def post(self, request, serialized_request):
        serialized_request.data['grant_type'] = 'password'
        user = authenticate(
            username=serialized_request.data.get('username'),
            password=serialized_request.data.get('password')
        )
        if user is None:
            error = serializers.RespError({
                'code': Error.INVALID_USER_OR_PASSWORD,
                'message': str(Error.INVALID_USER_OR_PASSWORD),
                'description': 'Invalid username or password'
            })
            return Response(error.data, status=status.HTTP_403_FORBIDDEN)

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
        serialized_response = serializers.RespToken(data={
            'token': token1,
            'refresh_token': token2
        })
        serialized_response.is_valid(raise_exception=True)
        return Response(serialized_response.data, status=status.HTTP_200_OK)