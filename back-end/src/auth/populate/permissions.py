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
            name=val["name"],
        )


def get_student_permissions():
    values = [
        "student.get.self",
        "teacher.get.all",
        "absence.get.self",
        "achievement.get.self",
        "encouragement.get.self",
        "punishment.get.self",
        "subject.get.all",
        "lesson.get.all",
        "mark.get.self",
        "reference_book.get.all",
    ]

    return [Permission.objects.get(codename=val) for val in values]


def get_teacher_permissions():
    values = [
        "student.get.milfaculty",
        "teacher.get.all",
        "absence.get.milfaculty",
        "achievement.get.milfaculty",
        "achievement.post.milfaculty",
        "achievement.patch.milfaculty",
        "encouragement.get.self",
        "encouragement.post.self",
        "encouragement.patch.self",
        "punishment.get.self",
        "punishment.post.self",
        "punishment.patch.self",
        "subject.get.all",
        "subject.post.all",
        "subject.patch.self",
        "subject.delete.self",
        "lesson.get.all",
        "lesson.post.self",
        "lesson.patch.self",
        "lesson.delete.self",
        "mark.get.self",
        "mark.post.self",
        "mark.patch.self",
        "mark.delete.self",
        "reference_book.get.all",
    ]

    return [Permission.objects.get(codename=val) for val in values]


def get_milfaculty_head_permissions():
    values = [
        "student.get.milfaculty",
        "student.post.milfaculty",
        "student.patch.milfaculty",
        "student.delete.milfaculty",
        "teacher.get.all",
        "teacher.post.milfaculty",
        "teacher.patch.milfaculty",
        "teacher.delete.milfaculty",
        "absence.get.milfaculty",
        "absence.post.milfaculty",
        "absence.patch.milfaculty",
        "absence.delete.milfaculty",
        "achievement.get.milfaculty",
        "achievement.post.milfaculty",
        "achievement.patch.milfaculty",
        "achievement.delete.milfaculty",
        "encouragement.get.milfaculty",
        "encouragement.post.milfaculty",
        "encouragement.patch.milfaculty",
        "encouragement.delete.milfaculty",
        "punishment.get.milfaculty",
        "punishment.post.milfaculty",
        "punishment.patch.milfaculty",
        "punishment.delete.milfaculty",
        "subject.get.all",
        "subject.post.all",
        "subject.patch.all",
        "subject.delete.all",
        "lesson.get.all",
        "lesson.post.milfaculty",
        "lesson.patch.milfaculty",
        "lesson.delete.milfaculty",
        "mark.get.milfaculty",
        "mark.post.milfaculty",
        "mark.patch.milfaculty",
        "mark.delete.milfaculty",
        "reference_book.get.all",
    ]

    return [Permission.objects.get(codename=val) for val in values]
