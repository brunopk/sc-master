from rest_framework.serializers import Serializer, CharField, ValidationError
from re import match
from webcolors import hex_to_rgb, rgb_to_hex
from resources.models.color import Color
from sc_master.utils.helpers import validate_hex


# noinspection PyAbstractClass
class Color(Serializer):

    id = CharField(read_only=True)

    rgb = CharField(required=False)

    hex = CharField(required=False)

    def validate(self, data):
        if 'rgb' not in data.keys() and 'hex' not in data.keys():
            raise ValidationError('At least hex or rgb value must be provided')
        if 'rgb' in data.keys() and 'hex' in data.keys():
            raise ValidationError('Provide only hexadecimal or rgb value')
        return data

    def validate_rgb(self, value):
        regex = r"^rgb\((\d{1,3})\s?,\s?(\d{1,3})\s?,\s?(\d{1,3})\)$"
        _match = match(regex, value)
        if _match is not None:
            red = int(_match.groups()[0])
            green = int(_match.groups()[1])
            blue = int(_match.groups()[2])
            if 0 > red or 0 > green or 0 > blue or 255 < red or 255 < green or 255 < blue:
                raise ValidationError('Invalid RGB color (example rgb(255,255,255)')
            return red, green, blue
        else:
            raise ValidationError('Invalid RGB color (example rgb(255,255,255)')

    def validate_hex(self, value):
        return validate_hex(value)

    def create(self, validated_data):
        if 'hex' in validated_data.keys():
            hex_value = validated_data.get('hex')
            rgb_tuple = hex_to_rgb(hex_value)
        else:
            rgb_tuple = validated_data.get('rgb')
            hex_value = rgb_to_hex(rgb_tuple)

        return Color.objects.create(hex=hex_value, red=rgb_tuple[0], green=rgb_tuple[1], blue=rgb_tuple[2])

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'hex': instance.hex,
            'rgb': f'rgb({instance.red}, {instance.green}, {instance.blue})',
        }
