from rest_framework.serializers import ModelSerializer, SerializerMethodField

from lms.models import (
    Milfaculty,
    Milgroup,
    Teacher,
)

from lms.serializers.serializers import MilgroupSerializer


class TeacherSerializer(ModelSerializer):
    milgroup = MilgroupSerializer(many=False)
    fullname = SerializerMethodField()

    class Meta:
        model = Teacher
        fields = '__all__'

    # pylint: disable=(no-self-use)
    def get_fullname(self, obj):
        return f'{obj.surname} {obj.name} {obj.patronymic}'

    # pylint: disable=(no-self-use)
    def create(self, validated_data):
        milgroup_data = validated_data.pop('milgroup')
        milfaculty = Milfaculty.objects.get(
            milfaculty=validated_data.pop('milgroup'))
        milgroup = Milgroup.objects.get(milfaculty=milfaculty, **milgroup_data)

        return Teacher.objects.create(milgroup=milgroup,
                                             **validated_data)

    def update(self, instance, validated_data):
        milgroup_data = validated_data.pop('milgroup')
        milfaculty = Milfaculty.objects.get(
            milfaculty=milgroup_data.pop('milfaculty'))
        milgroup = Milgroup.objects.get(milfaculty=milfaculty, **milgroup_data)

        return instance.update(milgroup=milgroup, **validated_data)