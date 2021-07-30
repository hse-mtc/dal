import uuid
from pathlib import Path

from django.db.models import QuerySet

import xlsxwriter

from lms.models.students import Student
from lms.utils.export.formats import Formats


def generate_export(students: QuerySet, milspecialties: QuerySet) -> Path:
    """Generate an Excel file with information about the students.

    Returns:
        A path to the generated Excel file.
    """

    path = Path(f"/tmp/{uuid.uuid4()}.xlsx")
    workbook = xlsxwriter.Workbook(path)
    formats = Formats.from_workbook(workbook)

    for milspecialty in milspecialties:
        worksheet = workbook.add_worksheet(milspecialty.code)
        _set_row_col_sizes(worksheet)
        _fill_header(worksheet=worksheet, cell_format=formats.table_center)

        for row, student in enumerate(
                students.filter(milspecialty=milspecialty),
                start=1,  # Skip header.
        ):
            cells = _make_student_row(
                student=student,
                formats=formats,
            )
            for col, (data, cell_format) in enumerate(cells):
                worksheet.write(row, col, data, cell_format)

    workbook.close()
    return path


def _set_row_col_sizes(worksheet: xlsxwriter.Workbook.worksheet_class,) -> None:
    worksheet.set_column(0, 0, 30)  # ФИО
    worksheet.set_column(1, 1, 15)  # Дата рождения
    worksheet.set_column(3, 3, 15)  # Кампус
    worksheet.set_column(5, 5, 13)  # Средний балл / 100
    worksheet.set_column(6, 6, 34)  # РМО


def _fill_header(
    worksheet: xlsxwriter.Workbook.worksheet_class,
    cell_format: xlsxwriter.workbook.Format,
) -> None:
    columns = [
        "ФИО",
        "Дата рождения",
        "Код ОП",
        "Кампус",
        "Ср. балл",
        "Ср. балл (100)",
        "РМО",
        "РППО",
        "ПП",
        "Хар-ка",
        "СН",
        "Паспорт",
        "ПС",
        "СБ",
        "Заявление",
        "Подтягивания",
        "Скорость",
        "Кросс",
        "ФИЗО",
        "Итог",
    ]

    worksheet.write_row(0, 0, columns, cell_format=cell_format)


def _make_student_row(
    student: Student,
    formats: Formats,
) -> list[...]:
    row = [(student.full_name, formats.table_center)]

    # pylint: disable=invalid-name
    if (bi := student.birth_info) is not None:
        row += [(bi.date, formats.russian_date)]
    else:
        row += [("", formats.table_center)]

    if (ui := student.university_info) is not None:
        row += [
            (ui.program.code, formats.table_center),
            (ui.get_campus_display(), formats.table_center),
        ]
    else:
        row += [("", formats.table_center)] * 2

    if (ap := student.application_process) is not None:
        row += [
            (ap.mean_grade, formats.float),
            (int(ap.mean_grade * 10), formats.int),
            (ap.get_medical_examination_display(), formats.table_center),
            (ap.get_prof_psy_selection_display(), formats.table_center),
        ]

        for field in [
                "preferential_right", "characteristic_handed_over",
                "criminal_record_handed_over", "passport_handed_over",
                "registration_certificate_handed_over",
                "university_card_handed_over", "application_handed_over"
        ]:
            row.append(
                ("Да" if getattr(ap, field) else "Нет", formats.table_center))

        row += [
            (ap.pull_ups, formats.int),
            (ap.speed_run, formats.float),
            (ap.long_run, formats.float),
            (ap.physical_test_grade, formats.int),
        ]

    else:
        row += [("", formats.table_center)] * 14
        row += [(0, formats.table_center)]  # ФИЗО

    mean_grade_scaled = row[5][0]
    physical_test_grade = row[18][0]
    try:
        row += [(mean_grade_scaled + physical_test_grade, formats.int)]
    except TypeError:
        row += [(0, formats.int)]

    return row
