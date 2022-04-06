from auth.models import Permission


def get_applicant_permissions():
    values = [
        "applicant.applicant.self",
        "applicants.get.self",
        "applicants.post.self",
        "applicants.put.self",
        "applicants.patch.self",
    ]
    res = []
    for val in values:
        viewset, method, scope = val.split(".")
        # We can't use .get(codename=val) here as codename is stored at runtime
        res.append(
            Permission.objects.get(
                viewset=viewset,
                method=method,
                scope=int(getattr(Permission.Scope, scope.upper())),
            )
        )
    return res


def get_student_permissions():
    values = [
        "students.get.self",
        "teachers.get.all",
        "absences.get.self",
        "achievements.get.self",
        "encouragements.get.self",
        "punishments.get.self",
        "subjects.get.all",
        "lesson-subjects.get.all",
        "lessons.get.all",
        "marks.get.self",
        "milgroups.get.milfaculty",
        "reference-books.get.all",
        "uniforms.get.milfaculty",
        "papers.get.all",
        "categories.get.all",
        "publishers.get.all",
        "subjects.get.self",
        "favorite-books.get.self",
        "favorite-books.post.self",
        "favorite-books.patch.self",
        "favorite-books.delete.self",
        "books.get.self",
        "books.get.all",
        "authors.get.all",
        "student-birthday-alert.get.milfaculty",
        "teacher-birthday-alert.get.all",
        "sections.get.self",
        "sections.get.all",
    ]
    res = []
    for val in values:
        viewset, method, scope = val.split(".")
        # We can't use .get(codename=val) here as codename is stored at runtime
        res.append(
            Permission.objects.get(
                viewset=viewset,
                method=method,
                scope=int(getattr(Permission.Scope, scope.upper())),
            )
        )
    return res


def get_teacher_permissions():
    values = [
        # DMS permissions
        "authors.get.all",
        "authors.post.all",
        "authors.patch.all",
        "authors.delete.all",
        "books.get.all",
        "books.post.self",
        "books.patch.self",
        "books.delete.self",
        "favorite-books.get.self",
        "favorite-books.post.self",
        "favorite-books.patch.self",
        "favorite-books.delete.self",
        "sections.get.all",
        # LMS permissions
        "students.get.milfaculty",
        "teachers.get.all",
        "teachers.patch.self",
        "absences.get.milfaculty",
        "achievements.get.milfaculty",
        "achievements.post.milfaculty",
        "achievements.patch.milfaculty",
        "encouragements.get.self",
        "encouragements.post.self",
        "encouragements.patch.self",
        "encouragements.delete.self",
        "punishments.get.self",
        "punishments.post.self",
        "punishments.patch.self",
        "punishments.delete.self",
        "subjects.get.all",
        "lesson-subjects.get.all",
        "lessons.get.all",
        # TODO(gakhromov): comment out permissions below when
        #   references to teachers will be added to lessons.
        # "lessons.post.self",
        # "lessons.patch.self",
        # "lessons.delete.self",
        "marks.get.milfaculty",
        "marks.post.milfaculty",
        "marks.put.milfaculty",
        "marks.patch.milfaculty",
        "marks.delete.milfaculty",
        "milgroups.get.milfaculty",
        "milgroups.post.milfaculty",
        "milgroups.patch.milfaculty",
        "milgroups.delete.milfaculty",
        "reference-books.get.all",
        "uniforms.get.milfaculty",
        "student-birthday-alert.get.milfaculty",
        "teacher-birthday-alert.get.all",
        "approve-teacher.get.milfaculty",
        "approve-teacher.patch.milfaculty",
        "statistics.get.self",
        "papers.get.all",
        "categories.get.all",
        "publishers.get.all",
    ]

    res = []
    for val in values:
        viewset, method, scope = val.split(".")
        # We can't use .get(codename=val) here as codename is stored at runtime
        res.append(
            Permission.objects.get(
                viewset=viewset,
                method=method,
                scope=int(getattr(Permission.Scope, scope.upper())),
            )
        )
    return res


def get_milfaculty_head_permissions():
    values = [
        # DMS permissions
        "authors.get.all",
        "authors.post.all",
        "authors.patch.all",
        "authors.delete.all",
        "books.get.all",
        "books.post.self",
        "books.patch.self",
        "books.delete.self",
        "favorite-books.get.self",
        "favorite-books.post.self",
        "favorite-books.patch.self",
        "favorite-books.delete.self",
        "sections.get.all",
        "subjects.get.all",
        "statistics.get.self",
        "student-birthday-alert.get.all",
        # LMS permissions
        "students.get.milfaculty",
        "students.patch.milfaculty",
        "students.delete.milfaculty",
        "student-notes.get.self",
        "student-notes.post.self",
        "student-notes.patch.self",
        "student-notes.delete.self",
        "teachers.get.all",
        "teachers.post.milfaculty",
        "teachers.patch.milfaculty",
        "teachers.delete.milfaculty",
        "absences.get.milfaculty",
        "absences.post.milfaculty",
        "absences.patch.milfaculty",
        "absences.delete.milfaculty",
        "absence-attachments.delete.milfaculty",
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
        "lesson-subjects.get.all",
        "lessons.get.all",
        "lessons.post.milfaculty",
        "lessons.patch.milfaculty",
        "lessons.delete.milfaculty",
        "marks.get.milfaculty",
        "marks.post.milfaculty",
        "marks.put.milfaculty",
        "marks.patch.milfaculty",
        "marks.delete.milfaculty",
        "milgroups.get.milfaculty",
        "reference-books.get.all",
        "uniforms.get.milfaculty",
        "uniforms.patch.milfaculty",
        "student-birthday-alert.get.milfaculty",
        "teacher-birthday-alert.get.all",
        "statistics.get.self",
        "papers.get.all",
        "categories.get.all",
        "publishers.get.all",
        "approve-teacher.get.milfaculty",
        "permissions.get.all",
        "approve-teacher.patch.milfaculty",
        "approve-student.get.self",
        "approve-student.get.milgroup",
        "approve-student.get.milfaculty",
        "approve-student.patch.self",
        "approve-student.patch.milgroup",
        "approve-student.patch.milfaculty",
    ]

    res = []
    for val in values:
        viewset, method, scope = val.split(".")
        # We can't use .get(codename=val) here as codename is stored at runtime
        res.append(
            Permission.objects.get(
                viewset=viewset,
                method=method,
                scope=int(getattr(Permission.Scope, scope.upper())),
            )
        )
    return res


def get_student_milgroup_commander_permissions():
    values = [
        "approve-student.get.self",
        "approve-student.get.milgroup",
        "approve-student.patch.self",
        "approve-student.patch.milgroup",
        "permissions.get.all",
    ]
    res = []
    for val in values:
        viewset, method, scope = val.split(".")
        # We can't use .get(codename=val) here as codename is stored at runtime
        res.append(
            Permission.objects.get(
                viewset=viewset,
                method=method,
                scope=int(getattr(Permission.Scope, scope.upper())),
            )
        )
    return res
