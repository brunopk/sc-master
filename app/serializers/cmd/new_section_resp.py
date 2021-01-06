from rest_framework.serializers import Serializer, UUIDField, CharField


class CmdNewSectionResp(Serializer):

    id = UUIDField()

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

