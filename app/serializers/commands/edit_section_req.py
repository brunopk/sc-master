from rest_framework.serializers import Serializer, IntegerField, ValidationError, UUIDField, CharField


class CmdEditSectionReq(Serializer):

    section_id = UUIDField(required=True)
    color = CharField(required=False)
    start = IntegerField(required=False)
    end = IntegerField(required=False)

    def validate(self, attrs):
        start = attrs.get('start')
        end = attrs.get('end')
        if start is not None and end is not None and start > end:
            raise ValidationError('Start cannot be larger than end')
        if start is not None and start < 0:
            raise ValidationError('start must be a positive integer')
        if end is not None and end < 0:
            raise ValidationError('end must be a positive integer')
        return attrs

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass
