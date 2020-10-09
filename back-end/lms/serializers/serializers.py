from rest_framework.serializers import (Serializer, ModelSerializer, IntegerField,
                                        CharField, SerializerMethodField)

from lms.models import (
    Milgroup,
    Program,
    Skill,
    Rank,
)


class MilgroupSerializer(ModelSerializer):
    milgroup = IntegerField()
    milfaculty = CharField(required=False)
    weekday = IntegerField(required=False)

    class Meta:
        model = Milgroup
        fields = '__all__'


class ProgramSerializer(ModelSerializer):

    class Meta:
        model = Program
        fields = '__all__'
        extra_kwargs = {'code': {'validators': []}}



class RankSerializer(ModelSerializer):
    
    class Meta:
        model = Rank
        fields = '__all__'


class ReferenceBookSerializer(Serializer):
    milgroups = SerializerMethodField(read_only=True)
    programs = SerializerMethodField(read_only=True)
    ranks = SerializerMethodField(read_only=True)

    def get_milgroups(self):
        qs = Milgroup.objects.all()
        return MilgroupSerializer(qs, many=True).data

    def get_programs(self):
        qs = Program.objects.all()
        return ProgramSerializer(qs, many=True).data

    def get_ranks(self):
        qs = Rank.objects.all()
        return RankSerializer(qs, many=True).data
