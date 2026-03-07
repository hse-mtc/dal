from rest_framework import serializers

from ams.models.physical import ExerciseResult


class ExerciseResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExerciseResult
        fields = [
            "exercise_type",
            "value",
            "extra_params",
            "secondary_score",
        ]
        read_only_fields = ["secondary_score"]


class ExerciseDefinitionSerializer(serializers.Serializer):
    """Сериализатор для справочника упражнений (не модель, а dataclass)."""

    exercise_type = serializers.CharField()
    name = serializers.CharField()
    direction = serializers.CharField()
    unit = serializers.CharField()
    extra_params = serializers.ListField(child=serializers.CharField())
    higher_is_better = serializers.BooleanField()
