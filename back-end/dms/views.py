import operator

import typing as tp

from functools import reduce

from taggit.models import Tag

from django.utils.encoding import escape_uri_path
from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.deletion import RestrictedError
from django.db.models.functions import ExtractYear
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import (
    Max,
    Q,
    F,
)

from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.decorators import (
    api_view,
    permission_classes,
)
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_422_UNPROCESSABLE_ENTITY,
)

from dms.serializers import (
    AuthorSerializer,
    CategorySerializer,
    DocumentSerializer,
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
        """
        Deletes Category from database based on primary key (currently, id).
        If category has documents, no deletion is performed and 422 is returned.
        """

        try:
            # pylint: disable=no-member
            return super().destroy(request, *args, **kwargs)
        except RestrictedError:
            return Response(
                {"message": "Category has documents and can not be deleted."},
                status=HTTP_422_UNPROCESSABLE_ENTITY)


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
    file = doc.get(pk=request.query_params.get("id")).file
    filename = file.name.split("/")[-1]

    with open(file.name, "rb") as content:
        response = HttpResponse(content, content_type="text/plain")
        response["Content-Disposition"] = f"attachment; " \
            f"filename={escape_uri_path(filename)}"
        return response


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request: Request) -> Response:
    username = request.data.get("username")
    password = request.data.get("password")
    if not username or not password:
        return Response({"message": "Username and password are required."},
                        status=HTTP_400_BAD_REQUEST)

    user = authenticate(
        username=username,
        password=password,
    )
    if not user:
        return Response({"message": "Invalid credentials."},
                        status=HTTP_404_NOT_FOUND)

    token, _ = Token.objects.get_or_create(user=user)

    return Response({"token": token.key}, status=HTTP_200_OK)


@csrf_exempt
@api_view(["GET"])
def info(request: Request) -> Response:
    data = {
        "roles": ["admin"],
        "avatar": request.user.profile.photo,
        "name": request.user.profile.name,
    }

    return Response(data, status=HTTP_200_OK)


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def logout(request: Request) -> Response:
    try:
        request.user.auth_token.delete()
    except (AttributeError, ObjectDoesNotExist):
        pass

    return Response({"message": "User logged out successfully."},
                    status=HTTP_200_OK)


def extract_documents_from_queryset(documents_queryset) -> tp.List[tp.Dict]:
    return list(
        map(
            lambda item: {
                "annotation":
                    item.annotation,
                "authors":
                    list(item.authors.values_list(
                        "last_name",
                        flat=True,
                    )),
                "id":
                    item.id,
                "tags":
                    list(item.tags.names()),
                "publication_date":
                    item.publication_date.isoformat(),
                "publishers":
                    item.publishers.values_list(
                        "name",
                        flat=True,
                    ),
                "title":
                    item.title,
            },
            list(documents_queryset),
        ))


def extract_documents_by_year_from_queryset(documents_queryset):
    t_dict = {}
    total = 0
    data = {
        "items": [],
    }

    for year in documents_queryset.annotate(
            year=ExtractYear("publication_date")).values_list(
                "year", flat=True).distinct():
        t_dict[year] = extract_documents_from_queryset(
            documents_queryset.filter(publication_date__year=year))

    for key, value in t_dict.items():
        data["items"].append({
            "year": key,
            "items": value,
        })
        total += len(value)

    data["total"] = total

    return data


def documents(request: Request) -> Response:
    # pylint: disable=too-many-locals

    authors = request.query_params.get("authors")
    start_date = request.query_params.get("start_date")
    end_date = request.query_params.get("end_date")
    publishers = request.query_params.get("publishers")
    text = request.query_params.get("text")
    category = request.query_params.get("category")

    db_request = Document.objects.filter(is_in_trash=False)

    if category:
        db_request = db_request.filter(category__pk=category)
    if authors:
        db_request = db_request.filter(authors__pk__in=authors.split(","))
    if start_date:
        db_request = db_request.filter(publication_date__gte=start_date)
    if end_date:
        db_request = db_request.filter(publication_date__lte=end_date)
    if publishers:
        db_request = db_request.filter(publishers__pk__in=publishers.split(","))
    if text:
        db_request = db_request.filter(
            reduce(operator.and_,
                   [Q(title__icontains=word) for word in text.split()]) |
            reduce(operator.and_,
                   [Q(annotation__icontains=word) for word in text.split()]) |
            reduce(operator.and_,
                   [Q(tags__name__icontains=word) for word in text.split()]))

    db_request = db_request.order_by("-publication_date").distinct()

    data = extract_documents_by_year_from_queryset(db_request)

    return Response(data, status=HTTP_200_OK)


class DocumentViewSet(viewsets.ModelViewSet):
    """API for CRUD operations on Document model."""

    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [permissions.AllowAny]

    def list(self, request, *args, **kwargs):
        # pylint: disable=unused-argument
        return documents(request)

    def perform_destroy(self, instance):
        instance.is_in_trash = True
        instance.save()


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
