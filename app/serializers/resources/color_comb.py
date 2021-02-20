from rest_framework.serializers import ModelSerializer, IntegerField
from app.models.static_design import StaticDesign
from app.models.section import Section
from app.serializers.resources.section import ResrSection


class ResrColorCombination(ModelSerializer):

    id = IntegerField(read_only=True)
    section_set = ResrSection(many=True)

    class Meta:
        model = StaticDesign
        fields = '__all__'

    def create(self, validated_data):
        section_set = validated_data.pop('section_set')
        color_combination = StaticDesign.objects.create(**validated_data)
        for section in section_set:
            Section.objects.create(color_combination=color_combination, **section)
        return color_combination


