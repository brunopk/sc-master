from rest_framework.serializers import Serializer, IntegerField, CharField, ValidationError


class SectionReq(Serializer):

    start = IntegerField(required=True)
    end = IntegerField(required=True)
    color = IntegerField(required=True)

    def validate(self, attrs):
        start = attrs.get('start')
        end = attrs.get('end')
        if start > end:
            raise ValidationError('start cannot be larger than end')
        if start < 0 or end < 0:
            raise ValidationError('start and end must be positive integers')
        return attrs

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

