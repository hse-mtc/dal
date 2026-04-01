import uuid
from datetime import date
from pathlib import Path

from django.db.models import QuerySet

import xlsxwriter

from ams.models.applicants import Applicant
from ams.physical.exercises import Direction, ExerciseType, get_exercise_registry

from ams.utils.export.formats import Formats


EXERCISE_NUMBERS = {
    ExerciseType.PULL_UPS: 3,
    ExerciseType.LIFT_TURNOVER: 5,
    ExerciseType.LIFT_FORCE: 6,
    ExerciseType.KETTLEBELL_SNATCH: 10,
    ExerciseType.SPEED_RUN_60M: 17,
    ExerciseType.SPEED_RUN_100M: 18,
    ExerciseType.SHUTTLE_RUN: 19,
    ExerciseType.LONG_RUN_1KM: 24,
    ExerciseType.LONG_RUN_3KM: 25,
}


def generate_export(applicants: QuerySet, milspecialties: QuerySet) -> Path:
    """Generate an Excel file with information about the applicants
    using the competitive selection protocol template.

    Returns:
        A path to the generated Excel file.
    """

    path = Path(f"/tmp/{uuid.uuid4()}.xlsx")
    workbook = xlsxwriter.Workbook(path)
    formats = Formats.from_workbook(workbook)
    registry = get_exercise_registry()

    applicants = applicants.select_related(
        "birth_info",
        "university_info",
        "university_info__program",
        "application_process",
    ).prefetch_related("application_process__exercise_results")

    for milspecialty in milspecialties:
        worksheet = workbook.add_worksheet(milspecialty.code)
        _set_row_col_sizes(worksheet)
        data_start_row = _fill_header(
            worksheet=worksheet,
            formats=formats,
            milspecialty_code=milspecialty.code,
        )

        section_1_row = data_start_row - 1
        worksheet.merge_range(
            section_1_row,
            0,
            section_1_row,
            22,
            "1. Список граждан, прошедших конкурсный отбор",
            formats.table_center,
        )

        row = data_start_row
        studs = applicants.filter(milspecialty=milspecialty)

        for index, applicant in enumerate(studs):
            cells = _make_applicant_row(
                applicant=applicant,
                formats=formats,
                index=index,
                registry=registry,
            )

            for col, (data, cell_format) in enumerate(cells):
                worksheet.write(row, col, data, cell_format)
            worksheet.set_row(row, height=50)
            row += 1

        section_2_row = row + 1
        worksheet.merge_range(
            section_2_row,
            0,
            section_2_row,
            22,
            "2. Список граждан, не прошедших предварительный отбор и (или) конкурсный отбор",
            formats.table_center,
        )

    workbook.close()

    return path


def _set_row_col_sizes(
    worksheet: xlsxwriter.Workbook.worksheet_class,
) -> None:
    column_widths = [
        6,  # № п/п
        36,  # ФИО + дата
        20,  # Код специальности
        16,  # Медосвидетельствование
        16,  # Проф-псих
        12,  # Возрастная группа
        10,  # Номер упражнения (сила)
        10,  # Результат (сила)
        8,  # Балл (сила)
        10,  # Номер упражнения (быстрота)
        10,  # Результат (быстрота)
        8,  # Балл (быстрота)
        10,  # Номер упражнения (выносливость)
        10,  # Результат (выносливость)
        8,  # Балл (выносливость)
        10,  # Общий балл
        20,  # Соответствие требованиям
        16,  # Оценка физ. подготовки
        20,  # Право допуска 10%
        20,  # Преимущественное право
        18,  # Текущая успеваемость
        14,  # Итоговый результат
        20,  # Решение комиссии
    ]

    for col, width in enumerate(column_widths):
        worksheet.set_column(col, col, width)


def _fill_header(
    worksheet: xlsxwriter.Workbook.worksheet_class,
    formats: Formats,
    milspecialty_code: int,
) -> int:
    table_header_top = 16
    table_header_bottom = 17
    column_numbers_row = 18
    data_start_row = 20

    # Insert header
    worksheet.merge_range(
        "S1:W1",
        "УТВЕРЖДАЮ",
        formats.align_center,
    )
    worksheet.merge_range(
        "S2:W2",
        "Председатель конкурсной комиссии",
        formats.align_center,
    )
    worksheet.merge_range(
        "S3:W3",
        "Министерства обороны Российской Федерации",
        formats.align_center,
    )
    worksheet.merge_range(
        "S4:W4",
        "__________________________________________________",
        formats.align_center,
    )
    worksheet.merge_range(
        "S5:W5",
        "(воинское звание, подпись, инициал имени, фамилия)",
        formats.align_center,
    )
    worksheet.merge_range(
        "S6:W6",
        '"____" __________ 20___ г.',
        formats.align_center,
    )

    worksheet.merge_range(
        "A8:W8",
        "ПРОТОКОЛ",
        formats.header,
    )
    worksheet.merge_range(
        "A9:W9",
        "конкурсного отбора граждан, изъявивших желание пройти обучение по программе военной подготовки",
        formats.header,
    )
    worksheet.merge_range(
        "A10:W10",
        "офицеров (сержантов, старшин, солдат, матросов) запаса в военном учебном центре",
        formats.header,
    )
    worksheet.merge_range(
        "A11:W11",
        "при___________________________________________________________________________________________",
        formats.header,
    )
    worksheet.merge_range(
        "A12:W12",
        "(наименование федеральной государственной образовательной организации высшего образования)",
        formats.header,
    )
    worksheet.merge_range(
        "A13:W13",
        f"по военно-учетной специальности {milspecialty_code}",
        formats.header,
    )
    worksheet.merge_range(
        "A14:W14",
        "(код военно-учетной специальности)",
        formats.header,
    )

    worksheet.set_row(table_header_top - 1, height=120)
    worksheet.set_row(table_header_bottom - 1, height=120)

    worksheet.merge_range(
        f"A{table_header_top}:A{table_header_bottom}",
        "№ п/п",
        formats.table_center,
    )
    worksheet.merge_range(
        f"B{table_header_top}:B{table_header_bottom}",
        "Фамилия, имя, отчество (при наличии), дата рождения",
        formats.table_center,
    )
    worksheet.merge_range(
        f"C{table_header_top}:C{table_header_bottom}",
        "Код специальности, направления подготовки высшего образования",
        formats.table_center,
    )
    worksheet.merge_range(
        f"D{table_header_top}:E{table_header_top}",
        "Результаты предварительного отбора",
        formats.table_center,
    )
    worksheet.write(
        f"D{table_header_bottom}",
        "Категория годности по состоянию здоровья",
        formats.table_center,
    )
    worksheet.write(
        f"E{table_header_bottom}",
        "Категория профессиональной психологической пригодности",
        formats.table_center,
    )
    worksheet.merge_range(
        f"F{table_header_top}:F{table_header_bottom}",
        "Возрастная группа",
        formats.table_center,
    )
    worksheet.merge_range(
        f"G{table_header_top}:O{table_header_top}",
        "Физические упражнения",
        formats.table_center,
    )
    worksheet.write(f"G{table_header_bottom}", "Номер упражнения", formats.table_center)
    worksheet.write(f"H{table_header_bottom}", "Результат", formats.table_center)
    worksheet.write(f"I{table_header_bottom}", "Балл", formats.table_center)
    worksheet.write(f"J{table_header_bottom}", "Номер упражнения", formats.table_center)
    worksheet.write(f"K{table_header_bottom}", "Результат", formats.table_center)
    worksheet.write(f"L{table_header_bottom}", "Балл", formats.table_center)
    worksheet.write(f"M{table_header_bottom}", "Номер упражнения", formats.table_center)
    worksheet.write(f"N{table_header_bottom}", "Результат", formats.table_center)
    worksheet.write(f"O{table_header_bottom}", "Балл", formats.table_center)
    worksheet.merge_range(
        f"P{table_header_top}:P{table_header_bottom}",
        "Общий балл",
        formats.table_center,
    )
    worksheet.merge_range(
        f"Q{table_header_top}:Q{table_header_bottom}",
        "Соответствие требованиям по уровню физической подготовки",
        formats.table_center,
    )
    worksheet.merge_range(
        f"R{table_header_top}:R{table_header_bottom}",
        "Оценка уровня физической подготовки (по стобалльной шкале)",
        formats.table_center,
    )
    worksheet.merge_range(
        f"S{table_header_top}:T{table_header_top}",
        "Наличие льготных оснований для допуска",
        formats.table_center,
    )
    worksheet.write(
        f"S{table_header_bottom}",
        "Право допуска в размере не менее 10% расчета набора",
        formats.table_center,
    )
    worksheet.write(
        f"T{table_header_bottom}",
        "Преимущественное право допуска",
        formats.table_center,
    )
    worksheet.merge_range(
        f"U{table_header_top}:U{table_header_bottom}",
        "Оценка уровня текущей успеваемости (по стобалльной шкале)",
        formats.table_center,
    )
    worksheet.merge_range(
        f"V{table_header_top}:V{table_header_bottom}",
        "Итоговый результат",
        formats.table_center,
    )
    worksheet.merge_range(
        f"W{table_header_top}:W{table_header_bottom}",
        "Решение конкурсной комиссии",
        formats.table_center,
    )

    worksheet.write_row(
        column_numbers_row - 1,
        0,
        list(range(1, 24)),
        formats.table_center,
    )

    return data_start_row - 1


def _make_applicant_row(
    applicant: Applicant,
    formats: Formats,
    index: int,
    registry: dict,
) -> list[...]:
    row = [(f"{index + 1}.", formats.table_center)]

    # pylint: disable=invalid-name
    birth_date = ""
    if (bi := applicant.birth_info) is not None and bi.date:
        birth_date = bi.date.strftime("%d.%m.%Y")

    fullname = applicant.fullname.strip()
    if birth_date:
        fullname = f"{fullname}\n{birth_date}"
    row += [(fullname, formats.table_center)]

    if (ui := applicant.university_info) is not None:
        row += [(ui.program.digit_code, formats.table_center)]
    else:
        row += [("", formats.table_center)]

    if (ap := applicant.application_process) is not None:
        row += [
            (ap.get_medical_examination_display(), formats.table_center),
            (ap.get_prof_psy_selection_display(), formats.table_center),
        ]
    else:
        row += [("", formats.table_center)] * 2

    row += [(_get_age_group(applicant), formats.table_center)]

    if ap is not None:
        exercises = _select_best_exercises(ap, registry)
    else:
        exercises = {}

    for direction in [Direction.STRENGTH, Direction.SPEED, Direction.ENDURANCE]:
        exercise = exercises.get(direction)
        if exercise is None:
            row += [("", formats.table_center)] * 3
            continue

        result_value = _format_exercise_value(exercise["value"])
        row += [
            (exercise["number"], formats.table_center),
            (result_value, formats.table_center),
            (exercise["score"], formats.int),
        ]

    if ap is not None:
        total_score = ap.strength_score + ap.speed_score + ap.endurance_score
        row += [(total_score, formats.int)]
        row += [("", formats.table_center)]
        row += [(ap.physical_test_grade, formats.int)]
        row += [("", formats.table_center)]
        row += [("Да" if ap.preferential_right else "Нет", formats.table_center)]
        mean_grade_scaled = int(ap.mean_grade * 10)
        row += [(mean_grade_scaled, formats.int)]
        row += [(ap.physical_test_grade + mean_grade_scaled, formats.int)]
    else:
        row += [(0, formats.int)]
        row += [("", formats.table_center)]
        row += [(0, formats.int)]
        row += [("", formats.table_center)]
        row += [("", formats.table_center)]
        row += [(0, formats.int)]
        row += [(0, formats.int)]

    row += [("", formats.table_center)]

    return row


def _get_age_group(applicant: Applicant) -> str:
    try:
        birth_date: date = applicant.birth_info.date
    except Exception:
        return ""

    today = date.today()
    age = (
        today.year
        - birth_date.year
        - ((today.month, today.day) < (birth_date.month, birth_date.day))
    )
    if age <= 0:
        return ""
    return "до 25" if age < 25 else "25 и старше"


def _select_best_exercises(application_process, registry: dict) -> dict:
    best: dict[str, dict] = {}
    for result in application_process.exercise_results.all():
        definition = registry.get(result.exercise_type)
        if definition is None:
            continue

        direction = definition.direction
        existing = best.get(direction)
        if existing is None or result.secondary_score > existing["score"]:
            best[direction] = {
                "number": EXERCISE_NUMBERS.get(result.exercise_type, ""),
                "value": result.value,
                "score": result.secondary_score,
            }

    return best


def _format_exercise_value(value):
    if value is None:
        return ""
    if isinstance(value, float) and value.is_integer():
        return int(value)
    return round(value, 2) if isinstance(value, float) else value
