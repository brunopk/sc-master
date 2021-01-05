from rest_framework.serializers import Serializer


class RespOk(Serializer):

    def create(self, validated_data):
        raise NotImplemented()

    def update(self, instance, validated_data):
        raise NotImplemented()
