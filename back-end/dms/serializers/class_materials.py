from rest_framework import serializers

from dms.models.class_materials import (
    Section,
    Topic,
    ClassMaterial,
)
from dms.serializers.common import SubjectSerializer
from dms.serializers.documents import (
    DocumentSerializer,
    DocumentMutateSerializer,
)


class SectionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Section
        fields = "__all__"


class TopicSerializer(serializers.ModelSerializer):

    class Meta:
        model = Topic
        fields = "__all__"


class ClassMaterialSerializer(DocumentSerializer):

    class Meta:
        model = ClassMaterial
        fields = "__all__"


class ClassMaterialMutateSerializer(DocumentMutateSerializer):

    class Meta:
        model = ClassMaterial
        fields = "__all__"


class TopicRetrieveSerializer(TopicSerializer):
    class_materials = serializers.SerializerMethodField(read_only=True)

    def get_class_materials(self, obj: Topic):
        data = {}
        for value, label in ClassMaterial.Type.choices:
            materials = obj.classmaterial_set.filter(type=value)
            data[label] = ClassMaterialSerializer(materials, many=True).data
        return data


class SectionRetrieveSerializer(SectionSerializer):
    topics = TopicRetrieveSerializer(many=True,
                                     read_only=True,
                                     source="topic_set")


class SubjectRetrieveSerializer(SubjectSerializer):
    sections = SectionSerializer(many=True,
                                 read_only=True,
                                 source="section_set")
