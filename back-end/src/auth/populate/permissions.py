from auth.models import Permission


def get_student_permissions():
    values = [
        "students.get.self",
        "teachers.get.all",
        "absences.get.self",
        "achievements.get.self",
        "encouragements.get.self",
        "punishments.get.self",
        "subjects.get.all",
        "lessons.get.all",
        "marks.get.self",
        "reference-books.get.all",
        "uniforms.get.milfaculty",
    ]
    res = []
    for val in values:
        viewset, method, scope = val.split(".")
        # We can't use .get(codename=val) here as codename is stored at runtime
        res.append(
            Permission.objects.get(viewset=viewset,
                                   method=method,
                                   scope=int(
                                       getattr(Permission.Scope,
                                               scope.upper()))))
    return res


def get_teacher_permissions():
    values = [
        "students.get.milfaculty",
        "teachers.get.all",
        "absences.get.milfaculty",
        "achievements.get.milfaculty",
        "achievements.post.milfaculty",
        "achievements.patch.milfaculty",
        "encouragements.get.self",
        "encouragements.post.self",
        "encouragements.patch.self",
        "punishments.get.self",
        "punishments.post.self",
        "punishments.patch.self",
        "subjects.get.all",
        "lessons.get.all",
        # TODO(gakhromov): comment out permissions below when
        #   references to teachers will be added to lessons.
        # "lessons.post.self",
        # "lessons.patch.self",
        # "lessons.delete.self",
        "marks.get.self",
        "marks.post.self",
        "marks.patch.self",
        "marks.delete.self",
        "reference-books.get.all",
        "uniforms.get.all",
    ]

    res = []
    for val in values:
        viewset, method, scope = val.split(".")
        # We can't use .get(codename=val) here as codename is stored at runtime
        res.append(
            Permission.objects.get(viewset=viewset,
                                   method=method,
                                   scope=int(
                                       getattr(Permission.Scope,
                                               scope.upper()))))
    return res


def get_milfaculty_head_permissions():
    values = [
        "students.get.milfaculty",
        "students.patch.milfaculty",
        "students.delete.milfaculty",
        "teachers.get.all",
        "teachers.post.milfaculty",
        "teachers.patch.milfaculty",
        "teachers.delete.milfaculty",
        "absences.get.milfaculty",
        "absences.post.milfaculty",
        "absences.patch.milfaculty",
        "absences.delete.milfaculty",
        "achievements.get.milfaculty",
        "achievements.post.milfaculty",
        "achievements.patch.milfaculty",
        "achievements.delete.milfaculty",
        "encouragements.get.milfaculty",
        "encouragements.post.milfaculty",
        "encouragements.patch.milfaculty",
        "encouragements.delete.milfaculty",
        "punishments.get.milfaculty",
        "punishments.post.milfaculty",
        "punishments.patch.milfaculty",
        "punishments.delete.milfaculty",
        "subjects.get.all",
        "lessons.get.all",
        "lessons.post.milfaculty",
        "lessons.patch.milfaculty",
        "lessons.delete.milfaculty",
        "marks.get.milfaculty",
        "marks.post.milfaculty",
        "marks.patch.milfaculty",
        "marks.delete.milfaculty",
        "reference-books.get.all",
        "uniforms.get.all",
    ]

    res = []
    for val in values:
        viewset, method, scope = val.split(".")
        # We can't use .get(codename=val) here as codename is stored at runtime
        res.append(
            Permission.objects.get(viewset=viewset,
                                   method=method,
                                   scope=int(
                                       getattr(Permission.Scope,
                                               scope.upper()))))
    return res
