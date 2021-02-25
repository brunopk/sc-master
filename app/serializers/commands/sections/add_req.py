from rest_framework.serializers import Serializer
from app.serializers.commands.sections.section_req import SectionReq


class CmdAddSectionReq(Serializer):

    sections = SectionReq(many=True)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

