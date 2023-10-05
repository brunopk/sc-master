from typing import List
from rest_framework.serializers import Serializer, IntegerField, CharField, ListSerializer
from sc_master.utils.helpers import validate_section_limits, validate_hex


class Section(Serializer):

    color = CharField(required=True, max_length=7)

    start = IntegerField(required=True)

    end = IntegerField(required=True)

    class Meta:
        ref_name = None

    def validate(self, attrs):
        return validate_section_limits(attrs)

    def validate_color(self, value):
        return validate_hex(value)


class Add(Serializer):

    class Meta:
        ref_name = 'CmdAddSection'

    sections = Section(many=True, allow_empty=False, required=True)