from rest_framework import serializers

from dms.models.documents import File


class FileSerializer(serializers.ModelSerializer):
    extension = serializers.CharField(source="get_extension",
                                      required=False,
                                      read_only=True)

    class Meta:
        model = File
        exclude = ["id"]


class DocumentSerializer(serializers.ModelSerializer):
    file = FileSerializer(read_only=True)
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

        if "title" not in validated_data:
            validated_data["title"] = validated_data["file"].name

        return super().create(validated_data)

    def update_file(self, instance, validated_data):
        content = validated_data.pop("content", None)
        if content is None:
            return

        file = File.objects.get(id=instance.file.id)
        file.content = content
        file.name = content.name
        file.save()

    def update(self, instance, validated_data):
        self.update_file(instance, validated_data)
        return super().update(instance, validated_data)
