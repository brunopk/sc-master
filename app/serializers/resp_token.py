from rest_framework.serializers import Serializer, CharField


class RespToken(Serializer):

    token = CharField()
    refresh_token = CharField()

    def create(self, validated_data):
        raise NotImplemented()

    def update(self, instance, validated_data):
        raise NotImplemented()