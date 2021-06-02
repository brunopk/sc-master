from rest_framework.serializers import Serializer, CharField, IntegerField, BooleanField


class CmdScRpiStatusResp(Serializer):

    number_of_led = IntegerField(required=False)
    status = CharField(required=True)
    status_details = CharField(required=False)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

