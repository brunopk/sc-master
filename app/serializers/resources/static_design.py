from rest_framework.serializers import ModelSerializer, IntegerField
from app.models.static_design import StaticDesign
from app.models.section import Section
from app.serializers.resources.section import ResrSection


class ResrStaticDesign(ModelSerializer):

    id = IntegerField(read_only=True)
    section_set = ResrSection(many=True)

    class Meta:
        model = StaticDesign
        exclude = ['active']

    def create(self, validated_data):
        section_set = validated_data.pop('section_set')
        static_design = StaticDesign.objects.create(**validated_data)
        for section in section_set:
            Section.objects.create(static_design=static_design, **section)
        return static_design


