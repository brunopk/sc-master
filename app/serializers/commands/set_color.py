from rest_framework.serializers import Serializer, UUIDField, CharField


class CmdSetColor(Serializer):

    section_id = UUIDField(required=False)
    color = CharField(required=True)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

