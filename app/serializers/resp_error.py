from rest_framework.serializers import Serializer, IntegerField, CharField


class RespError(Serializer):

    code = IntegerField()
    message = CharField()
    description = CharField()

    def create(self, validated_data):
        raise NotImplemented()

    def update(self, instance, validated_data):
        raise NotImplemented()
