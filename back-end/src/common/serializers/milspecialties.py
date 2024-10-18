from rest_framework import serializers

from common.models.milspecialties import Milspecialty


class MilspecialtySerializer(serializers.ModelSerializer):
    class Meta:
        model = Milspecialty
        exclude = ["selectable_by", "selectable_by_every_program"]


class MilspecialtyWithSensitiveInformationSerializer(MilspecialtySerializer):
    class Meta:
        model = Milspecialty
        fields = "__all__"


class WithSelectableByProgramMilspecialtySerializer(MilspecialtySerializer):
    selectable_by_program = serializers.SerializerMethodField()

    def get_selectable_by_program(self, milspecialty: Milspecialty):
        request = self.context["request"]
        program = request.query_params.get("program")
        if program is not None:
            return milspecialty.is_selectable_by_program(program)
        return False
