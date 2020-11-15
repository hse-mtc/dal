from dms.models.books import Book
from dms.serializers.documents import (
    DocumentSerializer,
    DocumentMutateSerializer,
)
from dms.serializers.common import (
    AuthorSerializer,
    PublisherSerializer,
    SubjectSerializer,
)


class BookSerializer(DocumentSerializer):
    authors = AuthorSerializer(many=True, read_only=True)
    publishers = PublisherSerializer(many=True, read_only=True)
    subjects = SubjectSerializer(many=True, read_only=True)

    class Meta:
        model = Book
        fields = "__all__"


class BookMutateSerializer(DocumentMutateSerializer):

    class Meta:
        model = Book
        exclude = ["file"]
