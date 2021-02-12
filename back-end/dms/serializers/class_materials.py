from rest_framework import serializers

from drf_spectacular.utils import (
    extend_schema_field,
    inline_serializer,
)

from dms.models.class_materials import (
    ClassMaterial,
    Section,
    Topic,
)
from dms.serializers.common import SubjectSerializer
from dms.serializers.documents import (
    DocumentMutateSerializer,
    DocumentSerializer,
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


ClassMaterialsByType = inline_serializer(
    name="ClassMaterialsByType",
    fields={
        label: ClassMaterialSerializer() for label in ClassMaterial.Type.labels
    },
)


class TopicRetrieveSerializer(TopicSerializer):
    class_materials = serializers.SerializerMethodField(read_only=True)

    @extend_schema_field(ClassMaterialsByType)
    def get_class_materials(self, obj: Topic):
        data = {}
        for value, label in ClassMaterial.Type.choices:
            materials = obj.class_materials.filter(type=value)
            data[label] = ClassMaterialSerializer(
                materials,
                many=True,
                context=self.context,
            ).data
        return data


class SectionRetrieveSerializer(SectionSerializer):
    topics = TopicRetrieveSerializer(many=True, read_only=True)


class SubjectRetrieveSerializer(SubjectSerializer):
    sections = SectionSerializer(many=True, read_only=True)


ClassMaterialMutateSerializerForSwagger = inline_serializer(
    name="ClassMaterialMutateInline",
    fields={
        "content": serializers.FileField(),
        "data": ClassMaterialMutateSerializer(),
    },
)
