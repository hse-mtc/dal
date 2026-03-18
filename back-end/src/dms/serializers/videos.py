from rest_framework import serializers

from drf_spectacular.utils import inline_serializer

from dms.models.videos import Video
from dms.serializers.documents import (
    DocumentMutateSerializer,
    DocumentSerializer,
)


class VideoSerializer(DocumentSerializer):
    user_id = serializers.IntegerField(source="user.id")

    class Meta:
        model = Video
        fields = "__all__"


class VideoMutateSerializer(DocumentMutateSerializer):
    class Meta:
        model = Video
        fields = "__all__"


VideoMutateSerializerForSwagger = inline_serializer(
    name="VideoMutateInline",
    fields={
        "content": serializers.FileField(),
        "data": VideoMutateSerializer(),
    },
)
