from rest_framework.serializers import Serializer, IntegerField, CharField, ValidationError


class SectionResp(Serializer):

    id = IntegerField(required=True)
    start = IntegerField(required=True)
    end = IntegerField(required=True)
    color = CharField(required=False, max_length=6)

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass
