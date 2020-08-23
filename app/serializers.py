from rest_framework import serializers
from app import models

class Effect(serializers.ModelSerializer):

    class Meta:
        model = models.Effect
        fields = '__all__'

class ErrorResponse(serializers.Serializer):

    code = serializers.IntegerField()
    message = serializers.CharField()
    description = serializers.CharField()

    def create(self, validated_data):
        raise NotImplemented()

    def update(self, instance, validated_data):
        raise NotImplemented()

class GetTokenRequest(serializers.Serializer):

    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    grant_type = serializers.CharField(default='password')

    def update(self, instance, validated_data):
        raise NotImplemented()

    def create(self, validated_data):
        raise NotImplemented()


class GetTokenResponse(serializers.Serializer):

    token = serializers.CharField()
    refresh_token = serializers.CharField()

    def create(self, validated_data):
        raise NotImplemented()

    def update(self, instance, validated_data):
        raise NotImplemented()
