import datetime
from rest_framework import serializers

from .models import (
    Milfaculty,
    Milgroup,
    Program,
    Student
)


class MilgroupSerializer(serializers.ModelSerializer):
    milgroup = serializers.IntegerField()

    class Meta:
        model = Milgroup
        fields = '__all__'


class ProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = Program
        fields = '__all__'
        extra_kwargs = {
            'code': {'validators': []}
        }


class StudentQuerySerializer(serializers.Serializer):
    id = serializers.IntegerField(min_value=1,required=False)
    milgroup = serializers.IntegerField(required=False)
    name = serializers.CharField(required=False)
    status = serializers.CharField(required=False)


class StudentSerializer(serializers.ModelSerializer):
    milgroup = MilgroupSerializer(many=False)
    program = ProgramSerializer(many=False)
    birthdate = serializers.DateField(format='%d.%m.%Y', input_formats=['%d.%m.%Y', 'iso-8601'])

    fullname = serializers.SerializerMethodField()

    class Meta:
            model = Student
            fields = '__all__'

    def get_fullname(self, obj):
        return f'{obj.surname} {obj.name} {obj.patronymic}'

    def create(self, validated_data):
        milgroup_data = validated_data.pop('milgroup')
        milfaculty_data = milgroup_data.pop('milfaculty')
        milfaculty = Milfaculty.objects.get(milfaculty=milfaculty_data)
        milgroup = Milgroup.objects.get(milfaculty=milfaculty, **milgroup_data)

        program_data = validated_data.pop('program')
        program = Program.objects.get(**program_data)

        student_new = Student.objects.create(
            milgroup=milgroup, program=program,
            **validated_data)

        return student_new

    def update(self, instance, validated_data):
        milgroup_data = validated_data.pop('milgroup')
        milfaculty_data = milgroup_data.pop('milfaculty')
        milfaculty = Milfaculty.objects.get(milfaculty=milfaculty_data)
        milgroup = Milgroup.objects.get(milfaculty=milfaculty, **milgroup_data)

        program_data = validated_data.pop('program')
        program = Program.objects.get(**program_data)

        # Convert from '%d.%m.%Y' format to '%Y-%m-%d' format
        # because Django doesn't accept russian formats.
        # Though, it accepts russian format on creating -_-
        validated_data['birthdate'] = datetime.datetime.strptime(
            validated_data['birthdate'], '%d.%m.%Y').strftime('%Y-%m-%d')
        # serializer converts
        student_modified = instance.update(
            milgroup=milgroup, program=program,
            **validated_data)

        return student_modified
