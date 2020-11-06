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

    class Meta:
        model = Author
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = "__all__"


class PublisherSerializer(serializers.ModelSerializer):

    class Meta:
        model = Publisher
        fields = "__all__"


class SubjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subject
        fields = "__all__"


class SectionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Section
        fields = "__all__"


class TopicSerializer(serializers.ModelSerializer):

    class Meta:
        model = Topic
        fields = "__all__"


class TagSerializer(serializers.ModelSerializer):

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


class DocumentSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        abstract = True


class DocumentMutateSerializer(DocumentSerializer):
    content = serializers.FileField(write_only=True)

    class Meta:
        abstract = True

    def create_file(self, validated_data):
        content = validated_data.pop("content")
        file = File.objects.create(content=content, name=content.name)
        validated_data["file"] = file

    def create(self, validated_data):
        self.create_file(validated_data)
        return super().create(validated_data)

    def update_file(self, instance, validated_data):
        if content := validated_data.pop("content", None):
            file = File.objects.get(id=instance.file.id)
            file.content = content
            file.name = content.name
            file.save()

    def update(self, instance, validated_data):
        self.update_file(instance, validated_data)
        return super().update(instance, validated_data)


class PaperSerializer(DocumentSerializer):
    authors = AuthorSerializer(many=True, read_only=True)
    file = FileSerializer(read_only=True)
    publishers = PublisherSerializer(many=True, read_only=True)
    tags = TagListField(required=False, read_only=True)

    class Meta:
        model = Paper
        fields = "__all__"


class PaperMutateSerializer(DocumentMutateSerializer):
    tags = TagListField(required=False)

    class Meta:
        model = Paper
        exclude = ["file"]

    def create(self, validated_data):
        tags = validated_data.pop("tags", None)
        instance = super().create(validated_data)
        if tags:
            instance.tags.set(*tags)
        return instance

    def update(self, instance, validated_data):
        tags = validated_data.pop("tags", None)
        instance = super().update(instance, validated_data)
        if tags:
            instance.tags.set(*tags, clear=True)
        return instance


class ClassMaterialSerializer(DocumentSerializer):
    file = FileSerializer(read_only=True)

    class Meta:
        model = ClassMaterial
        fields = ["id", "title", "file"]


class ClassMaterialMutateSerializer(DocumentMutateSerializer):

    class Meta:
        model = ClassMaterial
        exclude = ["file"]


class TopicRetrieveSerializer(serializers.ModelSerializer):
    class_materials = serializers.SerializerMethodField(read_only=True)

    def get_class_materials(self, obj: Topic):
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
        fields = "__all__"


class BookSerializer(DocumentSerializer):
    authors = AuthorSerializer(many=True, read_only=True)
    file = FileSerializer(read_only=True)
    publishers = PublisherSerializer(many=True, read_only=True)
    subjects = SubjectSerializer(many=True, read_only=True)

    class Meta:
        model = Book
        fields = "__all__"


class BookMutateSerializer(DocumentMutateSerializer):

    class Meta:
        model = Book
        exclude = ["file"]
