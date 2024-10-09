from rest_framework import serializers

from common.models.milspecialties import Milspecialty


class MilspecialtySerializer(serializers.ModelSerializer):
    class Meta:
        model = Milspecialty
        exclude = ["selectable_by", "selectable_by_every_program"]


class MilspecialtySelectableByProgramSerializer(MilspecialtySerializer):
    selectable_by_program = serializers.SerializerMethodField()

    def get_selectable_by_program(self, obj):
        request = self.context["request"]
        program = request.query_params.get("program")
        if program is not None:
            return (
                obj.selectable_by.filter(pk=program).exists()
                or obj.selectable_by_every_program
            )
        return False
