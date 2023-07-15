from drf_spectacular.utils import extend_schema
from rest_framework import status, generics
from rest_framework.request import Request
from rest_framework.response import Response

from auth.models import Permission
from auth.permissions import BasePermission
from common.models.subjects import Subject
from common.parsers import MultiPartWithJSONParser
from lms.models.common import Milgroup
from lms.models.lessons import Lesson, Room
from lms.models.teachers import Teacher
from lms.serializers.import_schedule import (
    ImportParsedSerializer,
    ImportParsedListSerializer,
    ParseScheduleSerializer,
)
from lms.utils.import_schedule import parse_timetable
from lms.views.lessons import LessonPermission


def guess_subject_name(subject_name):
    if "ТП" in subject_name:
        return "Тактическая подготовка"
    if "ТСП" in subject_name:
        return "Тактико-специальная подготовка"
    if "ВСП" in subject_name:
        return "Военно-специальная подготовка"
    if "ВПП" in subject_name:
        return "Военно-политическая подготовка"
    if "ОТ" in subject_name:
        return "Общая тактика"
    if "ОП" in subject_name:
        return "Огневая подготовка"
    if "ТПЧ" in subject_name:
        return "Тактика подразделений и частей РВСН"
    if "ОВУ" in subject_name:
        return "Общевоинские уставы ВС РФ"
    if "СтрП" in subject_name:
        return "Строевая подготовка"
    if "Тех.П" in subject_name:
        return "Техническая подготовка"
    if "УПМВ" in subject_name:
        return "Управление подразделениями в мирное время"
    if "РП" in subject_name:
        return "Разведывательная подготовка"
    if "ИП" in subject_name:
        return "Инженерная подготовка"
    if "РХБЗ" in subject_name:
        return "Подготовка по РХБЗ"
    if "СВ" in subject_name:
        return "Подготовка по связи"
    return ""


def guess_subject_type(subject_name):
    if " Л " in subject_name:
        return Lesson.Type.LECTURE
    if " С " in subject_name:
        return Lesson.Type.SEMINAR
    if " ГЗ " in subject_name:
        return Lesson.Type.GROUP
    if " ПЗ " in subject_name:
        return Lesson.Type.PRACTICE
    if "зачет" in subject_name.lower().replace("ё", "е"):
        return Lesson.Type.FINAL_TEST
    if "экзамен" in subject_name.lower():
        return Lesson.Type.EXAM
    return Lesson.Type.OTHER


class ImportSchedulePermission(BasePermission):
    permission_class = "import-permission"
    view_name_rus = "Импорт расписания из файла"
    scopes = [
        Permission.Scope.ALL,
    ]


@extend_schema(tags=["import-schedule"])
class ParseScheduleView(generics.GenericAPIView):
    parser_classes = [MultiPartWithJSONParser]
    permission_classes = [LessonPermission]
    serializer_class = ParseScheduleSerializer

    def post(self, request: Request):
        if "content" not in request.data:
            return Response(
                {"detail": "Bad request: no file passed"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        file = request.data["content"]

        lessons_list = parse_timetable(file)
        milgroups = set()
        teachers = set()
        classrooms = set()

        for elem in lessons_list:
            milgroups.add(elem["milgroup"])
            for t in elem["teachers"]:
                teachers.add(t)
            for c in elem["classrooms"]:
                classrooms.add(c)

        milgroups_cache = {}
        classrooms_cache = {}
        teachers_cache = {}

        for milgroup in milgroups:
            milg_filtered = Milgroup.objects.filter(title__iexact=milgroup)
            if milg_filtered:
                milgroups_cache[milgroup.lower()] = milg_filtered[0]
        for classroom in classrooms:
            classroom_filtered = Room.objects.filter(title__iexact=classroom)
            if classroom_filtered:
                classrooms_cache[classroom.lower()] = classroom_filtered[0]

        for teacher in teachers:
            surname, name = teacher
            teacher_filtered = Teacher.objects.filter(
                surname__iexact=surname, name__istartswith=name[0]
            )

            if teacher_filtered:
                teachers_cache[teacher] = teacher_filtered[0]
        parsed_lessons_list = []
        for elem in lessons_list:
            lesson = {"input": {}, "parsed": {}}
            lesson_name_input = elem["subject"]
            lesson["input"]["lesson_name_input"] = lesson_name_input

            lesson_subject_title = guess_subject_name(lesson_name_input)
            lesson["input"]["lesson_subject_title"] = lesson_subject_title

            lesson_type = guess_subject_type(lesson_name_input)
            lesson["parsed"]["type"] = lesson_type

            lesson["parsed"]["type"] = lesson_type
            lesson["parsed"]["date"] = elem["date"]
            lesson["parsed"]["ordinal"] = elem["ordinal"]
            if elem["milgroup"] in milgroups_cache:
                milgroup = milgroups_cache[elem["milgroup"]]
                lesson["parsed"]["milgroup"] = milgroup.pk
                lesson["parsed"]["milgroup_title"] = milgroup.title
                subjects = Subject.objects.filter(
                    milspecialty=milgroup.milspecialty, title=lesson_subject_title
                )

                if len(subjects) > 0:
                    lesson_subject = subjects[0]
                    lesson["parsed"]["subject"] = lesson_subject.pk
                    lesson["parsed"]["subject_title"] = lesson_subject.pk
                else:
                    lesson["parsed"]["subject"] = None
                    lesson["parsed"]["subject_title"] = None
            else:
                lesson["parsed"]["milgroup"] = None
                lesson["parsed"]["milgroup_title"] = None
                lesson["parsed"]["subject"] = None
                lesson["parsed"]["subject_title"] = None

            teacher_names = elem["teachers"]
            lesson["input"]["teachers"] = teacher_names
            if len(teacher_names) > 0 and teacher_names[0] in teachers_cache:
                teacher = teachers_cache[teacher_names[0]]
                lesson["parsed"]["teacher"] = teacher.pk
                lesson["parsed"][
                    "teacher_name"
                ] = f"{teacher.surname} {teacher.name} {teacher.patronymic}"
            else:
                lesson["parsed"]["teacher"] = None
                lesson["parsed"]["teacher_name"] = None

            classrooms = elem["classrooms"]
            if len(classrooms) > 0 and classrooms[0] in classrooms_cache:
                classroom = classrooms_cache[classrooms[0]]
                lesson["parsed"]["room"] = classroom.pk
                lesson["parsed"]["room_title"] = classroom.title
            else:
                lesson["parsed"]["room"] = None
                lesson["parsed"]["room_title"] = None

            parsed_lessons_list.append(lesson)
        return Response({"lessons": parsed_lessons_list})


@extend_schema(tags=["import-schedule"])
class ImportParsedView(generics.GenericAPIView):
    permission_classes = [ImportSchedulePermission]
    serializer_class = ImportParsedListSerializer

    def post(self, request: Request):
        valid_data = []
        if "lessons" not in request.data:
            return Response(
                {"error": "No 'lessons' field found in data"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        for data in request.data["lessons"]:
            serializer = ImportParsedSerializer(data=data)
            if serializer.is_valid(raise_exception=False):
                valid_data.append(data)
        request.data["lessons"] = valid_data
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"created": len(valid_data)}, status=status.HTTP_201_CREATED)
