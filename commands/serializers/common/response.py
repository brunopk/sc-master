from rest_framework.serializers import Serializer, Field, CharField, BooleanField, ValidationError, IntegerField
from sc_master.utils.helpers import remove_none_entries
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


class Device(Serializer):

    class Meta:
        ref_name = None

    address = CharField(required=True, max_length=7)

    port = IntegerField(required=True)

    number_of_led = IntegerField(required=True)

    def update(self, instance, validated_data):
        super(Device, self).update(instance, validated_data)

    def create(self, validated_data):
        super(Device, self).create(validated_data)


class Mode(Field):

    class Meta:
        ref_name = None

    def to_internal_value(self, data: HardwareMode):
        return data

    def to_representation(self, instance):
        return instance.name


class Response(Serializer):
    """
    Usually DRF serializers are intended to serialize the user input (JSON) to a model that can be handled by the
    framework and may end up in database. In this case, this class allows to serialize only dictionaries :

    ```
    Response(data=assdict(some_object))
    ```

    into another dictionary, say `output_dictionary`, whose values are Python primitive datatypes (or nested
    dictionaries), in order for DRF to output JSON data. Note that values in `data` may be instances of any
    class while values in `output_dictionary` will be Python primitive datatypes (or nested dicts).

    This conversion is accomplished in `to_representation` method.
    """

    class Meta:
        ref_name = 'CmdResponse'

    is_system_on = BooleanField(required=True)

    mode = Mode(allow_null=False)

    device = Device(required=False, allow_null=True)

    static_design = Section(required=False, many=True, allow_null=True)

    def to_representation(self, instance):
        """
        Generate the `output_dictionary` (see class description).
        `None` values will be removed from the final result
        """
        # TODO: si hardware mode no es static => remover la lista de static design (agregar esto al Gist para mejora a futuro cuando haya mas de un modo)
        ord_dict_rep = super().to_representation(instance)
        return remove_none_entries(ord_dict_rep)
