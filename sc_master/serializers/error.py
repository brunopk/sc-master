from rest_framework.serializers import Serializer, IntegerField, CharField
from sc_master.utils.errors import NotImplemented


class Error(Serializer):

    code = IntegerField()

    message = CharField()

    def create(self, validated_data):
        raise NotImplemented()

    def update(self, instance, validated_data):
        raise NotImplemented()
