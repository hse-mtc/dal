from common.models.subjects import Subject


def create_subjects() -> list[Subject]:
    subjects = []

    titles = [
        "Тактическая подготовка",
        "Тактико-специальная подготовка",
        "Военно-специальная подготовка",
        "Военно-инженерная подготовка",
        "Военно-политическая подготовка",
        "Военная топография",
        "Строевая подготовка",
    ]

    for title in titles:
        subject, _ = Subject.objects.get_or_create(
            title=title,
            annotation=f"Пример аннотации для {title.lower()}",
        )
        subjects.append(subject)

    return subjects
