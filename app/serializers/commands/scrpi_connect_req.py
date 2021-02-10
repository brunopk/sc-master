from rest_framework.serializers import Serializer, CharField, IntegerField


class CmdScRpiConnectReq(Serializer):

    address = CharField(required=True)
    port = IntegerField(required=True)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

