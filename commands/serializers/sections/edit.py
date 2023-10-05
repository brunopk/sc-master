from rest_framework.serializers import Serializer, IntegerField, ValidationError, CharField
from sc_master.utils.helpers import validate_section_limits, validate_hex


class Edit(Serializer):

    color = CharField(required=False, max_length=7)
    start = IntegerField(required=False)
    end = IntegerField(required=False)

    class Meta:
        ref_name = 'CmdEditSection'

    def validate_color(self, value):
        return validate_hex(value)

    def validate(self, attrs):
        return validate_section_limits(attrs)
