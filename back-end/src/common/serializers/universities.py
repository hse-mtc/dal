from rest_framework import serializers

from common.models.universities import (
    Faculty,
    Program,
    UniversityInfo,
)


class FacultySerializer(serializers.ModelSerializer):
    class Meta:
        model = Faculty
        fields = "__all__"


class ProgramSerializer(serializers.ModelSerializer):
    faculty = FacultySerializer(read_only=True)

    class Meta:
        model = Program
        fields = "__all__"


class ProgramMutateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Program
        fields = "__all__"


class UniversityInfoSerializer(serializers.ModelSerializer):
    campus = serializers.SerializerMethodField(read_only=True)

    def get_campus(self, obj: UniversityInfo) -> str:
        return obj.campus

    class Meta:
        model = UniversityInfo
        exclude = ["id"]


class UniversityInfoMutateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UniversityInfo
        fields = "__all__"
