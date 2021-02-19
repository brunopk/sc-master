from rest_framework.serializers import Serializer, CharField, BooleanField, IntegerField


class CmdScRpiStatusResp(Serializer):

    led_number = CharField(required=True)
    is_error = BooleanField(required=True)
    last_exception = CharField(required=False)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

