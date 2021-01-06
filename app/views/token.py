from rest_framework.views import APIView
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from oauth2_provider.models import AccessToken, Application, RefreshToken
from oauthlib.common import generate_token
from drf_yasg.utils import swagger_auto_schema
from django.contrib.auth import authenticate
from django.utils.timezone import now
from django.db.models import Q
from datetime import timedelta
from app.serializers.req.token import ReqToken
from app.serializers.resp.error import RespError
from app.serializers.resp.token import RespToken
from app.decorators import serializer
from app.enums import Error
from project.settings import CLIENT_ID, ACCESS_TOKEN_EXPIRE_SECONDS, TOKEN_SCOPE


class Token(APIView):
    permission_classes = (AllowAny,)

    @swagger_auto_schema(responses={HTTP_200_OK: ReqToken(), HTTP_400_BAD_REQUEST: RespError()}, request_body=ReqToken)
    @serializer(serializer_class=ReqToken)
    def post(self, request, serialized_request):
        serialized_request.data['grant_type'] = 'password'
        user = authenticate(
            username=serialized_request.data.get('username'),
            password=serialized_request.data.get('password')
        )
        if user is None:
            error = RespError({
                'code': Error.INVALID_USER_OR_PASSWORD,
                'message': str(Error.INVALID_USER_OR_PASSWORD),
                'description': 'Invalid username or password'
            })
            return Response(error.data, status=HTTP_403_FORBIDDEN)

        application = Application.objects.get(client_id=CLIENT_ID)
        query = Q(user=user) & Q(expires__gte=now())
        access_tokens = AccessToken.objects.filter(query).order_by('-expires')
        for a in access_tokens:
            a.revoke()
        expires = now() + timedelta(seconds=ACCESS_TOKEN_EXPIRE_SECONDS)
        token1 = generate_token()
        token2 = generate_token()
        access_token = AccessToken(user=user, scope=TOKEN_SCOPE, expires=expires, token=token1, application=application)
        access_token.save()
        refresh_token = RefreshToken(user=user, token=token2, application=application, access_token=access_token)
        refresh_token.save()
        serialized_response = RespToken(data={'token': token1, 'refresh_token': token2})
        serialized_response.is_valid(raise_exception=True)
        return Response(serialized_response.data, status=HTTP_200_OK)
