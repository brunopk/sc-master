from rest_framework.serializers import Serializer, ListSerializer, IntegerField


class CmdRemoveSectionsReq(Serializer):

    sections = ListSerializer(child=IntegerField(), allow_empty=False)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

