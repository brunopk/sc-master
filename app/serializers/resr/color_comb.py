from rest_framework.serializers import ModelSerializer, IntegerField
from app.models.color_comb import ColorCombination
from app.models.section import Section
from app.serializers.resr.section import ResrSection


class ResrColorCombination(ModelSerializer):

    id = IntegerField(read_only=True)
    section_set = ResrSection(many=True)

    class Meta:
        model = ColorCombination
        fields = '__all__'

    def create(self, validated_data):
        section_set = validated_data.pop('section_set')
        color_combination = ColorCombination.objects.create(**validated_data)
        for section in section_set:
            Section.objects.create(color_combination=color_combination, **section)
        return color_combination


