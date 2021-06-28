from auth.models import Permission


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
        "uniform.get.milfaculty",
    ]
    res = []
    for val in values:
        viewset, method, scope = val.split(".")
        # We can't use .get(codename=val) here as codename is stored at runtime
        res.append(
            Permission.objects.get(viewset=viewset,
                                   method=method,
                                   scope=int(
                                       getattr(Permission.Scopes,
                                               scope.upper()))))
    return res


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
        "lesson.get.all",
        "lesson.post.self",
        "lesson.patch.self",
        "lesson.delete.self",
        "mark.get.self",
        "mark.post.self",
        "mark.patch.self",
        "mark.delete.self",
        "reference_book.get.all",
        "uniform.get.all",
    ]

    res = []
    for val in values:
        viewset, method, scope = val.split(".")
        # We can't use .get(codename=val) here as codename is stored at runtime
        res.append(
            Permission.objects.get(viewset=viewset,
                                   method=method,
                                   scope=int(
                                       getattr(Permission.Scopes,
                                               scope.upper()))))
    return res


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
        "lesson.get.all",
        "lesson.post.milfaculty",
        "lesson.patch.milfaculty",
        "lesson.delete.milfaculty",
        "mark.get.milfaculty",
        "mark.post.milfaculty",
        "mark.patch.milfaculty",
        "mark.delete.milfaculty",
        "reference_book.get.all",
        "uniform.get.all",
    ]

    res = []
    for val in values:
        viewset, method, scope = val.split(".")
        # We can't use .get(codename=val) here as codename is stored at runtime
        res.append(
            Permission.objects.get(viewset=viewset,
                                   method=method,
                                   scope=int(
                                       getattr(Permission.Scopes,
                                               scope.upper()))))
    return res
