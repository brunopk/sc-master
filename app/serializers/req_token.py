from rest_framework.serializers import Serializer, CharField


class ReqToken(Serializer):

    username = CharField(required=True)
    password = CharField(required=True)

    def update(self, instance, validated_data):
        raise NotImplemented()

    def create(self, validated_data):
        raise NotImplemented()
