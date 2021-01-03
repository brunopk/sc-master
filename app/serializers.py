from re import match
from webcolors import hex_to_rgb, rgb_to_hex
from rest_framework import serializers
from app import models


# noinspection PyAbstractClass
class ResColor(serializers.Serializer):

    id = serializers.IntegerField(read_only=True)
    rgb = serializers.CharField(required=False)
    hex = serializers.CharField(required=False)

    def validate(self, data):
        if 'rgb' not in data.keys() and 'hex' not in data.keys():
            raise serializers.ValidationError('At least hex or rgb value must be provided')
        return data

    # noinspection PyMethodMayBeStatic
    def validate_rgb(self, value):
        regex = r"^rgb\((\d{1,3})\s?,\s?(\d{1,3})\s?,\s?(\d{1,3})\)$"
        _match = match(regex, value)
        if _match is not None:
            red = int(_match.groups()[0])
            green = int(_match.groups()[1])
            blue = int(_match.groups()[2])
            if 0 > red or 0 > green or 0 > blue or 255 < red or 255 < green or 255 < blue:
                raise serializers.ValidationError('Invalid RGB color (example rgb(255,255,255)')
            return red, green, blue
        else:
            raise serializers.ValidationError('Invalid RGB color (example rgb(255,255,255)')

    # noinspection PyMethodMayBeStatic
    def validate_hex(self, value):
        try:
            hex_to_rgb(value)
            return value
        except ValueError:
            raise serializers.ValidationError('Invalid hexadecimal color representation')

    def create(self, validated_data):
        if 'hex' in validated_data.keys():
            rgb_tuple = hex_to_rgb(validated_data.get('hex'))
            hex_value = validated_data.get('hex')
        else:
            rgb_tuple = self.validate_rgb(validated_data.get('rgb'))
            hex_value = rgb_to_hex(rgb_tuple)

        return models.Color.objects.create(red=rgb_tuple[0], blue=rgb_tuple[1], green=rgb_tuple[2], hex=hex_value)

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'rgb': f'rgb({instance.red}, {instance.green}, {instance.blue})',
            'hex': instance.hex
        }


class CmdSetColor(serializers.Serializer):

    section_id = serializers.UUIDField(required=False)
    color = serializers.CharField(required=True)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class RespOk(serializers.Serializer):

    def create(self, validated_data):
        raise NotImplemented()

    def update(self, instance, validated_data):
        raise NotImplemented()


class RespError(serializers.Serializer):

    code = serializers.IntegerField()
    message = serializers.CharField()
    description = serializers.CharField()

    def create(self, validated_data):
        raise NotImplemented()

    def update(self, instance, validated_data):
        raise NotImplemented()


class ReqToken(serializers.Serializer):

    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    def update(self, instance, validated_data):
        raise NotImplemented()

    def create(self, validated_data):
        raise NotImplemented()


class RespToken(serializers.Serializer):

    token = serializers.CharField()
    refresh_token = serializers.CharField()

    def create(self, validated_data):
        raise NotImplemented()

    def update(self, instance, validated_data):
        raise NotImplemented()
