from rest_framework.serializers import ModelSerializer, ValidationError
from app.models import Section


# TODO maybe is better to exclude remove is_on or put it readonly

class ResrSection(ModelSerializer):

    class Meta:
        model = Section
        exclude = ['static_design', 'hw_id']

    def validate(self, attrs):
        start = attrs.get('start')
        end = attrs.get('end')
        if start > end:
            raise ValidationError('Start cannot be larger than end')
        if start < 0 or end < 0:
            raise ValidationError('start and end must be positive integers')
        return attrs
