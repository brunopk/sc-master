from rest_framework.serializers import Serializer, ListSerializer, IntegerField


class Remove(Serializer):

    sections = ListSerializer(child=IntegerField(), allow_empty=False)

    class Meta:
        ref_name = 'CmdRemoveSections'

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass
