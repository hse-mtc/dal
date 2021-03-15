from django.contrib.auth.models import Permission


def create_permissions_for_view(view_name, view_name_rus):
    get_str = ": получение данных"
    post_str = ": добавление данных"
    patch_str = ": редактирование данных"
    delete_str = ": удаление данных"

    return [
        {
            "codename": view_name + "_get",
            "name": view_name_rus + get_str,
        },
        {
            "codename": view_name + "_post",
            "name": view_name_rus + post_str,
        },
        {
            "codename": view_name + "_patch",
            "name": view_name_rus + patch_str,
        },
        {
            "codename": view_name + "_delete",
            "name": view_name_rus + delete_str,
        },
    ]


def create_permissions(content_type):
    values = []
    values += create_permissions_for_view("student", "Студенты")
    values += create_permissions_for_view("teacher", "Учителя")
    values += create_permissions_for_view("absence", "Пропуски")
    values += create_permissions_for_view("achievement", "Достижения")
    values += create_permissions_for_view("encouragement", "Поощрения")
    values += create_permissions_for_view("punishment", "Взыскания")
    values += create_permissions_for_view("subject", "Предметы")
    values += create_permissions_for_view("lesson", "Расписание занятий")
    values += create_permissions_for_view("mark", "Оценки")
    values += create_permissions_for_view("reference_book", "Справочные данные")

    for val in values:
        Permission.objects.get_or_create(
            codename=val["codename"],
            name=val["name"],
            content_type=content_type,
        )


def get_student_permissions():
    values = [
        "student_get",
        "teacher_get",
        "absence_get",
        "achievement_get",
        "encouragement_get",
        "punishment_get",
        "subject_get",
        "lesson_get",
        "mark_get",
        "reference_book_get",
    ]

    return [Permission.objects.get(codename=val) for val in values]


def get_teacher_permissions():
    values = [
        "student_get",
        "teacher_get",
        "absence_get",
        "achievement_get",
        "achievement_post",
        "achievement_patch",
        "encouragement_get",
        "encouragement_post",
        "encouragement_patch",
        "punishment_get",
        "punishment_post",
        "punishment_patch",
        "subject_get",
        "subject_post",
        "subject_patch",
        "subject_delete",
        "lesson_get",
        "lesson_post",
        "lesson_patch",
        "lesson_delete",
        "mark_get",
        "mark_post",
        "mark_patch",
        "mark_delete",
        "reference_book_get",
    ]

    return [Permission.objects.get(codename=val) for val in values]


def get_milfaculty_head_permissions():
    values = [
        "student_get",
        "student_post",
        "student_patch",
        "student_delete",
        "teacher_get",
        "teacher_post",
        "teacher_patch",
        "teacher_delete",
        "absence_get",
        "absence_post",
        "absence_patch",
        "absence_delete",
        "achievement_get",
        "achievement_post",
        "achievement_patch",
        "achievement_delete",
        "encouragement_get",
        "encouragement_post",
        "encouragement_patch",
        "encouragement_delete",
        "punishment_get",
        "punishment_post",
        "punishment_patch",
        "punishment_delete",
        "subject_get",
        "subject_post",
        "subject_patch",
        "subject_delete",
        "lesson_get",
        "lesson_post",
        "lesson_patch",
        "lesson_delete",
        "mark_get",
        "mark_post",
        "mark_patch",
        "mark_delete",
        "reference_book_get",
        "reference_book_post",
        "reference_book_patch",
        "reference_book_delete",
    ]

    return [Permission.objects.get(codename=val) for val in values]
