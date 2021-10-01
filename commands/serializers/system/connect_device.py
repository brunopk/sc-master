from rest_framework.serializers import Serializer, IntegerField, CharField


class ConnectDevice(Serializer):

    class Meta:
        ref_name = "CmdConnectDevice"

    address = CharField(required=True)

    port = IntegerField(required=True)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass
