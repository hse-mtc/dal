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

    def validate(self, attrs):
        """Валидация extra_params согласно определению упражнения."""
        from ams.physical.exercises import get_exercise_registry

        exercise_type = attrs.get("exercise_type")
        if exercise_type is None and self.instance:
            exercise_type = self.instance.exercise_type

        # Для PATCH-запроса: если extra_params не переданы, берем из instance
        if "extra_params" in attrs:
            extra_params = attrs["extra_params"]
        elif self.instance:
            extra_params = self.instance.extra_params
        else:
            extra_params = {}

        registry = get_exercise_registry()
        definition = registry.get(exercise_type)

        if definition is None:
            raise serializers.ValidationError(
                {"exercise_type": f"Unknown exercise type: {exercise_type}"}
            )

        # Проверяем наличие и валидность обязательных параметров
        for param_name in definition.extra_params:
            param_value = extra_params.get(param_name)

            # Проверка наличия параметра
            if param_value is None:
                raise serializers.ValidationError(
                    {
                        "extra_params": f"Missing required parameter '{param_name}' "
                        f"for exercise '{definition.name}'"
                    }
                )

            # Проверка типа значения (должно быть число)
            if not isinstance(param_value, (int, float)):
                raise serializers.ValidationError(
                    {
                        "extra_params": f"Parameter '{param_name}' must be a number, "
                        f"got {type(param_value).__name__}"
                    }
                )

            # Проверка положительности значения
            if param_value <= 0:
                raise serializers.ValidationError(
                    {
                        "extra_params": f"Parameter '{param_name}' must be greater than zero, "
                        f"got {param_value}"
                    }
                )

        return attrs


class ExerciseDefinitionSerializer(serializers.Serializer):
    """Сериализатор для справочника упражнений (не модель, а dataclass)."""

    exercise_type = serializers.CharField()
    name = serializers.CharField()
    direction = serializers.CharField()
    unit = serializers.CharField()
    extra_params = serializers.ListField(child=serializers.CharField())
    higher_is_better = serializers.BooleanField()
