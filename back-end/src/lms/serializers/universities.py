from rest_framework.serializers import (
    ModelSerializer,
    CharField,
)

from lms.models.universities import (
    Program,
    UniversityInfo,
)


class ProgramSerializer(ModelSerializer):

    class Meta:
        model = Program
        fields = "__all__"
        extra_kwargs = {"code": {"validators": []}}


class UniversityInfoSerializer(ModelSerializer):
    program = ProgramSerializer(read_only=True)

    class Meta:
        model = UniversityInfo
        exclude = ["id"]


class UniversityInfoCreateSerializer(ModelSerializer):
    program = CharField(max_length=8)

    def create(self, validated_data):
        code = validated_data.pop("program")
        query = Program.objects.filter(code=code)

        if not query.exists():
            Program.objects.create(code=code)
        validated_data["program"] = query.first()

        return super().create(validated_data)

    class Meta:
        model = UniversityInfo
        exclude = ["id"]
