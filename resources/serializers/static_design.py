from rest_framework.serializers import ModelSerializer, IntegerField
from resources.models.static_design import StaticDesign as StaticDesignModel
from resources.models.section import Section as SectionModel
from sc_master.utils.helpers import validate_hex, validate_section_limits


class Section(ModelSerializer):

    class Meta:

        model = SectionModel

        exclude = ['static_design']

    def validate(self, attrs):
        return validate_section_limits(attrs)


class StaticDesign(ModelSerializer):

    id = IntegerField(read_only=True)

    section_set = Section(many=True)

    class Meta:

        model = StaticDesignModel

        fields = '__all__'

    def create(self, validated_data):
        section_set = validated_data.pop('section_set')
        static_design = StaticDesign.objects.create(**validated_data)
        for section in section_set:
            Section.objects.create(static_design=static_design, **section)
        return static_design
