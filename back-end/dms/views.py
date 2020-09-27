from django.db.models import Max
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.utils.encoding import escape_uri_path
from django.views.decorators.csrf import csrf_exempt

from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import (
    api_view,
    permission_classes,
)
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_422_UNPROCESSABLE_ENTITY,
)

from drf_yasg.utils import swagger_auto_schema

from django_filters.rest_framework import DjangoFilterBackend

from taggit.models import Tag

from dms.filters import DocumentFilter
from dms.swagger import author_array
from dms.serializers import (
    AuthorSerializer,
    CategorySerializer,
    DocumentSerializer,
    DocumentListSerializer,
    PublisherSerializer,
    TagSerializer,
    SubjectSerializer,
)
from dms.models import (
    Author,
    Document,
    Publisher,
    Subject,
    Topic,
    Category,
)


@method_decorator(name="list", decorator=swagger_auto_schema(tags=["Authors"]))
class AuthorViewSet(viewsets.ModelViewSet):
    """API for CRUD operations on Author model."""

    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.AllowAny]


class CategoryViewSet(viewsets.ModelViewSet):
    """API for CRUD operations on Category model."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]

    def destroy(self, request, *args, **kwargs):
        # pylint: disable=no-member

        category = self.get_object()
        available_documents = Document.objects.filter(is_in_trash=False)
        if available_documents.filter(category=category).exists():
            return Response(
                {"message": "Category has documents and can not be deleted."},
                status=HTTP_422_UNPROCESSABLE_ENTITY)

        return super().destroy(request, *args, **kwargs)


class PublisherViewSet(viewsets.ModelViewSet):
    """API for CRUD operations on Publisher model."""

    queryset = Publisher.objects.all()
    serializer_class = PublisherSerializer
    permission_classes = [permissions.AllowAny]


class SubjectViewSet(viewsets.ModelViewSet):
    """API for CRUD operations on Subject model."""

    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = [permissions.AllowAny]


class TagListAPIView(ListAPIView):
    """List all tags."""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.AllowAny]


class DocumentViewSet(viewsets.ModelViewSet):
    """API for CRUD operations on Document model."""

    queryset = Document.objects.filter(is_in_trash=False) \
                               .order_by("-publication_date")
    serializer_class = DocumentSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = DocumentFilter
    search_fields = ["title", "annotation", "tags__name"]

    def get_serializer_class(self):
        if self.action == "list":
            return DocumentListSerializer
        return DocumentSerializer

    @swagger_auto_schema(manual_parameters=[author_array])
    def list(self, request, *args, **kwargs):
        # pylint: disable=no-member
        return super().list(request, *args, **kwargs)

    def perform_destroy(self, instance):
        instance.is_in_trash = True
        instance.save()


@csrf_exempt
@api_view(["GET"])
@permission_classes((AllowAny,))
def get_file(request: Request) -> HttpResponse:
    """
    Usage: api/get_file?id=3
    :param request:
    :return:
    """

    doc = Document.objects.all()
    file = doc.get(pk=request.query_params.get("id")).file.content
    filename = file.name.split("/")[-1]

    with open(file.name, "rb") as content:
        response = HttpResponse(content, content_type="text/plain")
        response["Content-Disposition"] = f"attachment; " \
            f"filename={escape_uri_path(filename)}"
        return response


@permission_classes((AllowAny,))
class SubjectSectionView(APIView):
    """
    Describes a relationship with SubjectFilterSerializer
    in order to return Subject Page
    """

    @staticmethod
    def convert2dict(doc):
        return {
            "id": doc.id,
            "title": doc.title,
            "file": "/api/dms/get_file?id=" + str(doc.id),
        }

    def get(self, request):
        # pylint: disable=too-many-locals

        searching_id = request.query_params.get("id")
        searching_title = Subject.objects.filter(id=searching_id)[0].title

        source_documents = Document.objects.filter(
            subject__title=searching_title)
        section_title_documents = source_documents.annotate(
            section_title=Max("topic__section__title"))
        section_id_documents = section_title_documents.annotate(
            section_id=Max("topic__section__id"))
        documents_merged = section_id_documents.annotate(
            topic_title=Max("topic__title"))

        source_topics = Topic.objects.filter(
            section__subject__title=searching_title)
        topics = source_topics.annotate(section_title=Max("section__title"))

        data = {
            "title": searching_title,
            "parts": [],
        }

        section_set = set()
        section_id = 0
        for document in documents_merged:
            if document.section_title in section_set:
                continue
            section_set.add(document.section_title)
            section = dict()
            section["title"] = document.section_title
            section["id"] = section_id
            topic_list = []
            topic_id = 0
            for topic in topics:
                if topic.section_title == document.section_title:
                    topic_json_format = {
                        "id": topic_id,
                        "title": topic.title,
                        "lectures": [],
                        "seminars": [],
                        "group_classes": [],
                        "practice_classes": [],
                    }

                    lectures = documents_merged.filter(
                        topic_id=topic.id,
                        section_title=document.section_title,
                        category__title="Лекции")
                    seminars = documents_merged.filter(
                        topic_id=topic.id,
                        section_title=document.section_title,
                        category__title="Семинары")
                    group_classes = documents_merged.filter(
                        topic_id=topic.id,
                        section_title=document.section_title,
                        category__title="Групповые занятия")
                    practice_classes = documents_merged.filter(
                        topic_id=topic.id,
                        section_title=document.section_title,
                        category__title="Практические занятия")

                    for lec in lectures:
                        topic_json_format["lectures"].append(
                            SubjectSectionView.convert2dict(lec))
                    for sem in seminars:
                        topic_json_format["seminars"].append(
                            SubjectSectionView.convert2dict(sem))
                    for group in group_classes:
                        topic_json_format["group_classes"].append(
                            SubjectSectionView.convert2dict(group))
                    for practice in practice_classes:
                        topic_json_format["practice_classes"].append(
                            SubjectSectionView.convert2dict(practice))

                    topic_list.append(topic_json_format)
                    topic_id += 1
            section["topics"] = topic_list
            data["parts"].append(section)
            section_id += 1

        return Response(data, status=HTTP_200_OK)
