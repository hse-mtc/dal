from auth.models import Permission


def create_permissions_for_view(view_name, view_name_rus):
    methods_str = {
        "get": ": получение данных",
        "post": ": добавление данных",
        "patch": ": редактирование данных",
        "delete": ": удаление данных",
    }

    scopes_str = {
        "self": (30, ", связанных с пользователем"),
        "milgroup": (20, " о взоде, связанным с пользователем"),
        "milfaculty": (10, " о цикле, связанным с пользователем"),
        "all": (0, " (всех данных)"),
    }

    permissions = []
    for method in methods_str:
        for scope in scopes_str:
            permissions.append({
                "viewset":
                    view_name,
                "method":
                    method,
                "scope":
                    scopes_str[scope][0],
                "codename":
                    "_".join([view_name, method, scope]),
                "name":
                    "".join([
                        view_name_rus, methods_str[method], scopes_str[scope][1]
                    ]),
            })
    return permissions


def create_permissions():
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
            viewset=val["viewset"],
            method=val["method"],
            scope=val["scope"],
            codename=val["codename"],
            name=val["name"],
        )


def get_student_permissions():
    values = [
        "student_get_self",
        "teacher_get_all",
        "absence_get_self",
        "achievement_get_self",
        "encouragement_get_self",
        "punishment_get_self",
        "subject_get_all",
        "lesson_get_all",
        "mark_get_self",
        "reference_book_get_all",
    ]

    return [Permission.objects.get(codename=val) for val in values]


def get_teacher_permissions():
    values = [
        "student_get_milfaculty",
        "teacher_get_all",
        "absence_get_milfaculty",
        "achievement_get_milfaculty",
        "achievement_post_milfaculty",
        "achievement_patch_milfaculty",
        "encouragement_get_self",
        "encouragement_post_self",
        "encouragement_patch_self",
        "punishment_get_self",
        "punishment_post_self",
        "punishment_patch_self",
        "subject_get_all",
        "subject_post_all",
        "subject_patch_self",
        "subject_delete_self",
        "lesson_get_all",
        "lesson_post_self",
        "lesson_patch_self",
        "lesson_delete_self",
        "mark_get_self",
        "mark_post_self",
        "mark_patch_self",
        "mark_delete_self",
        "reference_book_get_all",
    ]

    return [Permission.objects.get(codename=val) for val in values]


def get_milfaculty_head_permissions():
    values = [
        "student_get_milfaculty",
        "student_post_milfaculty",
        "student_patch_milfaculty",
        "student_delete_milfaculty",
        "teacher_get_all",
        "teacher_post_milfaculty",
        "teacher_patch_milfaculty",
        "teacher_delete_milfaculty",
        "absence_get_milfaculty",
        "absence_post_milfaculty",
        "absence_patch_milfaculty",
        "absence_delete_milfaculty",
        "achievement_get_milfaculty",
        "achievement_post_milfaculty",
        "achievement_patch_milfaculty",
        "achievement_delete_milfaculty",
        "encouragement_get_milfaculty",
        "encouragement_post_milfaculty",
        "encouragement_patch_milfaculty",
        "encouragement_delete_milfaculty",
        "punishment_get_milfaculty",
        "punishment_post_milfaculty",
        "punishment_patch_milfaculty",
        "punishment_delete_milfaculty",
        "subject_get_all",
        "subject_post_all",
        "subject_patch_all",
        "subject_delete_all",
        "lesson_get_all",
        "lesson_post_milfaculty",
        "lesson_patch_milfaculty",
        "lesson_delete_milfaculty",
        "mark_get_milfaculty",
        "mark_post_milfaculty",
        "mark_patch_milfaculty",
        "mark_delete_milfaculty",
        "reference_book_get_all",
    ]

    return [Permission.objects.get(codename=val) for val in values]
