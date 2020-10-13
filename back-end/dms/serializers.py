from rest_framework import serializers

from taggit.models import Tag

from dms.models import (
    Author,
    Book,
    Category,
    ClassMaterial,
    File,
    Paper,
    Publisher,
    Section,
    Subject,
    Topic,
)


class AuthorSerializer(serializers.ModelSerializer):
    """Serializes Author model."""

    class Meta:
        model = Author
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    """Serializes Category model."""

    class Meta:
        model = Category
        fields = "__all__"


class PublisherSerializer(serializers.ModelSerializer):
    """Serializes Publisher model."""

    class Meta:
        model = Publisher
        fields = "__all__"


class SubjectSerializer(serializers.ModelSerializer):
    """Serializes Subject model."""

    class Meta:
        model = Subject
        fields = "__all__"


class TagSerializer(serializers.ModelSerializer):
    """Serializes Tag model."""

    class Meta:
        model = Tag
        fields = ["name"]

    def to_representation(self, instance):
        return instance.name


class TagListField(serializers.ListField):
    child = serializers.CharField()

    def to_representation(self, data):
        return data.values_list("name", flat=True)


class FileSerializer(serializers.ModelSerializer):
    extension = serializers.CharField(source="get_extension",
                                      required=False,
                                      read_only=True)

    class Meta:
        model = File
        exclude = ["id"]


class PaperCreateUpdateSerializer(serializers.ModelSerializer):
    """Create or update existing Paper model."""

    content = serializers.FileField(write_only=True)
    tags = TagListField(required=False)

    class Meta:
        model = Paper
        exclude = ["file"]

    def create(self, validated_data):
        tags = validated_data.pop("tags", None)

        content = validated_data.pop("content")
        file = File.objects.create(content=content, name=content.name)
        validated_data["file"] = file

        instance = super().create(validated_data)

        if tags:
            instance.tags.set(*tags)

        return instance

    def update(self, instance, validated_data):
        tags = validated_data.pop("tags", None)

        file = File.objects.get(id=instance.file.id)
        file.content = validated_data.pop("content")
        file.save()

        instance = super().update(instance, validated_data)

        if tags:
            instance.tags.set(*tags, clear=True)

        return instance


class PaperSerializer(serializers.ModelSerializer):
    """Serializes Paper model."""

    authors = AuthorSerializer(many=True, read_only=True)
    file = FileSerializer(read_only=True)
    publishers = PublisherSerializer(many=True, read_only=True)
    tags = TagListField(required=False, read_only=True)

    class Meta:
        model = Paper
        fields = "__all__"


class ClassMaterialSerializer(serializers.ModelSerializer):
    file = FileSerializer(read_only=True)

    class Meta:
        model = ClassMaterial
        fields = ["id", "title", "file"]


class TopicRetrieveSerializer(serializers.ModelSerializer):
    class_materials = serializers.SerializerMethodField(read_only=True)

    def get_class_materials(self, obj: Topic):
        # pylint: disable=no-self-use

        data = {}
        for value, label in ClassMaterial.Type.choices:
            materials = obj.classmaterial_set.filter(type=value)
            data[label] = ClassMaterialSerializer(materials, many=True).data
        return data

    class Meta:
        model = Topic
        fields = ["id", "title", "class_materials"]


class SectionRetrieveSerializer(serializers.ModelSerializer):
    topics = TopicRetrieveSerializer(many=True,
                                     read_only=True,
                                     source="topic_set")

    class Meta:
        model = Section
        fields = ["id", "title", "topics"]


class SubjectRetrieveSerializer(serializers.ModelSerializer):
    sections = SectionRetrieveSerializer(many=True,
                                         read_only=True,
                                         source="section_set")

    class Meta:
        model = Subject
        fields = ["id", "title", "abbreviation", "sections"]


class BookSerializer(serializers.ModelSerializer):
    authors = AuthorSerializer(many=True, read_only=True)
    file = FileSerializer(read_only=True)
    publication_year = serializers.ReadOnlyField()
    publishers = PublisherSerializer(many=True, read_only=True)
    subjects = SubjectSerializer(many=True, read_only=True)

    class Meta:
        model = Book
        exclude = ["publication_date"]


class BookCreateUpdateSerializer(serializers.ModelSerializer):
    content = serializers.FileField(write_only=True)
    publication_year = serializers.DateField(format="%Y", input_formats=["%Y"])

    class Meta:
        model = Book
        exclude = ["file", "publication_date"]

    def create(self, validated_data):
        content = validated_data.pop("content")
        file = File.objects.create(content=content, name=content.name)
        validated_data["file"] = file
        return super().create(validated_data)

    def update(self, instance, validated_data):
        file = File.objects.get(id=instance.file.id)
        file.content = validated_data.pop("content")
        file.save()
        return super().update(instance, validated_data)
