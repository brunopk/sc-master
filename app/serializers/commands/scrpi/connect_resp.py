from rest_framework.serializers import Serializer, IntegerField


class CmdScRpiConnectResp(Serializer):

    led_number = IntegerField(required=True)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

