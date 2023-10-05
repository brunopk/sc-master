from rest_framework.serializers import Serializer, CharField, ReadOnlyField
from sc_master.utils.helpers import remove_none_entries
from sc_master.utils.errors import NotImplemented


class ErrorCode(ReadOnlyField):

    def to_representation(self, value):
        return value.name


class Error(Serializer):

    code = ErrorCode(allow_null=False)

    message = CharField(allow_null=True)

    def to_representation(self, instance):
        """
        Generate the `output_dictionary` (see class description).
        `None` values will be removed from the final result
        """
        ord_dict_rep = super().to_representation(instance)
        return remove_none_entries(ord_dict_rep)

    def create(self, validated_data):
        raise NotImplemented()

    def update(self, instance, validated_data):
        raise NotImplemented()
