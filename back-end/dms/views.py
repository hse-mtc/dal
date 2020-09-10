import operator
import json

import typing as tp

from datetime import datetime
from functools import reduce

from taggit.models import Tag

from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Max
from django.db.models import Q, F
from django.db.models.functions import ExtractYear
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_412_PRECONDITION_FAILED,
)

from dms.models import (
    Author,
    Document,
    Publisher,
    Subject,
    Topic,
    Category,
)


@permission_classes((AllowAny,))
class CategoryView(APIView):

    @csrf_exempt
    def put(self, request: Request) -> Response:
        # pylint: disable=no-self-use
        if "title" not in request.data:
            return Response({"error": "No title provided"},
                            status=HTTP_400_BAD_REQUEST)

        category = Category()
        category.title = request.data.get("title")
        category.save()

        return Response(
            {
                "code": HTTP_200_OK * 100,
            },
            status=HTTP_200_OK,
        )

    @csrf_exempt
    def get(self, request: Request) -> Response:
        data = Category.objects.values("id", "title")

        return Response(
            {
                "code": HTTP_200_OK * 100,
                "data": data
            },
            status=HTTP_200_OK,
        )

    @csrf_exempt
    def delete(self, request: Request) -> Response:
        # pylint: disable=no-self-use
        category = Category.objects.get(pk=request.query_params.get("id"))

        if Document.objects.filter(category=category).exists():
            return Response(
                {
                    "code": HTTP_412_PRECONDITION_FAILED * 100,
                    "message": "Категорию нельзя удалить, "
                               "пока в ней есть хотя бы один документ."
                },
                status=HTTP_200_OK)

        category.delete()

        return Response({"code": HTTP_200_OK * 100}, status=HTTP_200_OK)


@permission_classes((AllowAny,))
class UploadNirView(APIView):

    def post(self, request: Request) -> Response:
        if "file" not in request.data:
            return Response(
                {
                    "error": "No file provided",
                },
                status=HTTP_400_BAD_REQUEST,
            )

        f = request.data["file"]

        doc = Document()

        doc.title = request.data["title"]

        category = request.data.get("category")
        if category:
            doc.category = Category.objects.get(pk=category)

        if request.data.get("annotation"):
            doc.annotation = request.data["annotation"]

        date = request.data.get("date")
        if date and date != "Invalid date":
            doc.publication_date = datetime.strptime(date, "%d.%m.%Y")

        doc.save()

        if request.data.get("keywords"):
            keywords_list = list(
                map(lambda x: x["value"], json.loads(request.data["keywords"])))

            if len(keywords_list) > 0:
                doc.keywords.add(*keywords_list)

        if request.data.get("authorId"):
            author = Author.objects.get(pk=request.data["authorId"])
            doc.authors.add(author)
        elif request.data.get("authorName"):
            author_name = request.data["authorName"]
            author_last_name = request.data["authorLastName"]
            author_patronymic = request.data["authorPatronymic"]
            doc.authors.create(
                last_name=author_last_name,
                first_name=author_name,
                patronymic=author_patronymic,
            )

        if request.data.get("publisherId"):
            publisher = Publisher.objects.get(pk=request.data["publisherId"])
            doc.publishers.add(publisher)
        elif request.data.get("newPublisher"):
            doc.publishers.create(name=request.data["newPublisher"])

        doc.file.save(
            name=f.name,
            content=f,
        )

        return Response(
            {
                "code": HTTP_200_OK * 100,
            },
            status=HTTP_200_OK,
        )

    def put(self, request: Request) -> Response:  # pylint: disable=no-self-use
        """
        Usage PUT request to api/upload?type=nir&id=21
        curl -X PUT -H 'Content-Disposition: attachment; filename=ptu.png' 'http://127.0.0.1:8000/api/upload?id=1' --upload-file some_file.png
        :param request:
        :return:
        """

        if "file" not in request.data:
            return Response(
                {
                    "error": "No file provided",
                },
                status=HTTP_400_BAD_REQUEST,
            )

        doc = Document.objects.all()
        f = request.data["file"]
        doc.get(pk=request.query_params.get("id")).file.save(
            name=f.name,
            content=f,
            save=True,
        )

        return Response(
            {
                "code": HTTP_201_CREATED * 100,
            },
            status=HTTP_201_CREATED,
        )


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
    print(f"{doc.get(id=request.query_params.get('id')) = }")
    f = doc.get(pk=request.query_params.get("id")).file
    print(f"{f = }")
    filename = f.name.split("/")[-1]
    print(f"{filename = }")

    with open(f.name, "rb") as content:
        response = HttpResponse(content, content_type="text/plain")
        response["Content-Disposition"] = f"attachment; filename={filename}"
        return response


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request: Request) -> Response:
    username = request.data.get("username")
    password = request.data.get("password")
    if not username or not password:
        return Response(
            {"error": "Please provide both username and password"},
            status=HTTP_400_BAD_REQUEST,
        )

    user = authenticate(
        username=username,
        password=password,
    )
    if not user:
        return Response(
            {"error": "Invalid Credentials"},
            status=HTTP_404_NOT_FOUND,
        )

    token, _ = Token.objects.get_or_create(user=user)

    return Response(
        {
            "code": HTTP_200_OK * 100,
            "data": {
                "token": token.key,
            },
        },
        status=HTTP_200_OK,
    )


@csrf_exempt
@api_view(["GET"])
def info(request: Request) -> Response:
    data = {
        "roles": ["admin"],
        "avatar": request.user.profile.photo,
        "name": request.user.profile.name,
    }

    return Response(
        {
            "code": HTTP_200_OK * 100,
            "data": data
        },
        status=HTTP_200_OK,
    )


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def logout(request: Request) -> Response:
    try:
        request.user.auth_token.delete()
    except (AttributeError, ObjectDoesNotExist):
        pass

    return Response(
        {
            "code": HTTP_200_OK * 100,
            "data": "success"
        },
        status=HTTP_200_OK,
    )


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
                "keywords":
                    list(item.keywords.names()),
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


@csrf_exempt
@api_view(["GET"])
@permission_classes((AllowAny,))
def documents(request: Request) -> Response:
    authors = request.query_params.get("authors")
    start_date = request.query_params.get("start_date")
    end_date = request.query_params.get("end_date")
    publishers = request.query_params.get("publishers")
    text = request.query_params.get("text")
    category = request.query_params.get("category")

    try:
        if str(category).upper() == "ARTICLE":
            category = Category.objects.get(title="Научные статьи")
        elif str(category).upper() == "RESEARCH":
            category = Category.objects.get(
                title="Научно-исследовательские работы")
    except:
        pass

    db_request = (Document.objects.filter(category=category).exclude(
        is_in_trash=True))

    if authors is not None:
        db_request = db_request.filter(
            authors__last_name__in=authors.split(","))
    if start_date is not None:
        db_request = db_request.filter(publication_date__gte=start_date)
    if end_date is not None:
        db_request = db_request.filter(publication_date__lte=end_date)
    if publishers is not None:
        db_request = db_request.filter(
            publishers__name__in=publishers.split(","))
    if text is not None:
        db_request = db_request.filter(
            reduce(operator.and_,
                   [Q(title__icontains=word) for word in text.split()]) |
            reduce(operator.and_,
                   [Q(annotation__icontains=word) for word in text.split()]) |
            reduce(operator.and_,
                   [Q(keywords__name__icontains=word)
                    for word in text.split()]))

    db_request = db_request.order_by("-publication_date")

    db_request = db_request.distinct()

    data = extract_documents_by_year_from_queryset(db_request)

    return Response(
        {
            "code": HTTP_200_OK * 100,
            "data": data
        },
        status=HTTP_200_OK,
    )


@csrf_exempt
@api_view(["GET"])
@permission_classes((AllowAny,))
def subjects(request):
    return Response(
        {
            "code": HTTP_200_OK * 100,
            "data": Subject.objects.values("id", "title"),
        },
        status=HTTP_200_OK)


@csrf_exempt
@api_view(["GET"])
@permission_classes((AllowAny,))
def authors(request):
    return Response(
        {
            "code":
                HTTP_200_OK * 100,
            "data":
                Author.objects.annotate(value=F("last_name")).values(
                    "value", "id"),
        },
        status=HTTP_200_OK)


@csrf_exempt
@api_view(["GET"])
@permission_classes((AllowAny,))
def publishers(request: Request) -> Response:
    return Response(
        {
            "code":
                HTTP_200_OK * 100,
            "data":
                Publisher.objects.annotate(value=F("name")).values(
                    "value", "id"),
        },
        status=HTTP_200_OK)


@csrf_exempt
@api_view(["GET"])
@permission_classes((AllowAny,))
def delete_document(request: Request,) -> Response:
    document_id = request.query_params.get("id")
    document = Document.objects.get(id=document_id)
    document.is_in_trash = True
    document.save()

    return Response(
        {
            "code": HTTP_200_OK * 100,
        },
        status=HTTP_200_OK,
    )


@csrf_exempt
@api_view(["GET"])
@permission_classes((AllowAny,))
def tags(request: Request,) -> Response:
    return Response(
        {
            "code": HTTP_200_OK * 100,
            "data": Tag.objects.values(key=F("id"), value=F("name"))
        },
        status=HTTP_200_OK,
    )


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
            "file": "/api/get_file?id=" + str(doc.id),
        }

    def get(self, request):
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

        return Response(
            {
                "data": data,
                "code": HTTP_200_OK * 100,
            },
            status=HTTP_201_CREATED,
        )
