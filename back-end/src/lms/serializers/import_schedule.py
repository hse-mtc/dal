from rest_framework import serializers

from lms.models.lessons import Lesson
from lms.serializers.lessons import LessonParsedSerializer


class ParseScheduleSerializer(serializers.Serializer):
    content = serializers.FileField(write_only=True)


class ImportParsedSerializer(serializers.Serializer):
    parsed = LessonParsedSerializer()


class ImportParsedListSerializer(serializers.Serializer):
    lessons = ImportParsedSerializer(many=True)

    def create(self, validated_data):
        parsed_data = validated_data["lessons"]

        lesson_parsed_objects = []

        for item in parsed_data:
            item_data = item["parsed"]
            lesson_parsed_objects.append(Lesson(**item_data))
        Lesson.objects.bulk_create(lesson_parsed_objects)

        return validated_data
