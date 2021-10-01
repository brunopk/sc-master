from rest_framework.serializers import Serializer, CharField, BooleanField, ValidationError, IntegerField
from sc_master.utils.enums import HardwareMode


class Section(Serializer):

    class Meta:
        ref_name = None

    color = CharField(required=True, max_length=7)

    start = IntegerField(required=True)

    end = IntegerField(required=True)

    is_on = BooleanField(required=True)

    def update(self, instance, validated_data):
        super(Section, self).update(instance, validated_data)

    def create(self, validated_data):
        super(Section, self).create(validated_data)


class ResponseError(Serializer):

    class Meta:
        ref_none = None

    code = CharField(required=True)

    message = CharField(required=True)


class Device(Serializer):

    class Meta:
        ref_name = None

    address = CharField(required=True, max_length=7)

    port = IntegerField(required=True)

    number_of_led = IntegerField(required=True)

    error = ResponseError(required=False, allow_null=True)

    def update(self, instance, validated_data):
        super(Device, self).update(instance, validated_data)

    def create(self, validated_data):
        super(Device, self).create(validated_data)


class Response(Serializer):

    class Meta:
        ref_name = 'CmdResponse'

    is_error = BooleanField(required=True)

    is_on = BooleanField(required=True)

    mode = CharField(required=True)

    error = ResponseError(required=False, allow_null=True)

    devices = Device(required=False, many=True)

    static_design = Section(required=False, many=True)

    _modes = [value.name for value in HardwareMode]

    # noinspection PyMethodMayBeStatic, PyProtectedMember
    def validate_mode(self, value):
        if value not in Response._modes:
            raise ValidationError(f'mode must be one of this {Response._modes}')
        return value

    def validate(self, data):
        fields = list(data.keys())
        is_error = data.get('is_error')
        is_device_error = any(map(lambda d: d.get('is_error'), data.get('devices')))
        error = data.get('error')
        if not is_device_error and (is_error and error is None):
            raise ValidationError('error is not defined')
        for field in fields:
            if isinstance(data.get(field), list) and len(data.get(field)) == 0:
                del data[field]
        return data

    def create(self, validated_data):
        super(Response, self).create(validated_data)

    def update(self, instance, validated_data):
        super(Response, self).update(instance, validated_data)
