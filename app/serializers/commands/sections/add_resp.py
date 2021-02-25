from rest_framework.serializers import Serializer
from app.serializers.commands.sections.section_resp import SectionResp


class CmdAddSectionResp(Serializer):

    sections = SectionResp(many=True)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

