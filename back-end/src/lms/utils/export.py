import uuid

from dataclasses import dataclass
from pathlib import Path

from django.db.models import QuerySet

import xlsxwriter

from xlsxwriter.format import Format
from xlsxwriter.workbook import Workbook

from lms.models.students import Student


@dataclass
class Formats:
    header: Format
    align_center: Format
    russian_date: Format
    int: Format
    float: Format

    @classmethod
    def from_workbook(cls, workbook: Workbook) -> "Formats":
        return Formats(
            header=workbook.add_format({"bold": True, "align": "center"}),
            align_center=workbook.add_format({"align": "center"}),
            russian_date=workbook.add_format({
                "num_format": "dd.mm.yyyy",
                "align": "center",
            }),
            int=workbook.add_format({
                "align": "center",
                "num_format": "#0"
            }),
            float=workbook.add_format({
                "align": "center",
                "num_format": "#,##0.00"
            }),
        )


def generate_excel(students: QuerySet, milspecialties: QuerySet) -> Path:
    """Generate an Excel file with information about the students.

    Returns:
        A path to the generated Excel file.
    """

    path = Path(f"/tmp/{uuid.uuid4()}.xlsx")
    workbook = xlsxwriter.Workbook(path)
    formats = Formats.from_workbook(workbook)

    for milspecialty in milspecialties:
        worksheet = workbook.add_worksheet(milspecialty.code)
        _fill_header(worksheet=worksheet, cell_format=formats.header)

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

    worksheet.write_row(0, 0, columns)
    worksheet.set_row(0, cell_format=cell_format)
    worksheet.set_column(0, 0, 30)  # ФИО
    worksheet.set_column(1, 1, 15)  # Дата рождения
    worksheet.set_column(3, 3, 15)  # Кампус
    worksheet.set_column(5, 5, 13)  # Средний балл / 100
    worksheet.set_column(6, 6, 34)  # РМО


def _make_student_row(
    student: Student,
    formats: Formats,
) -> list[...]:
    row = [(student.full_name, formats.align_center)]

    if (bi := student.birth_info) is not None:
        row += [(bi.date, formats.russian_date)]
    else:
        row += [("", formats.align_center)]

    if (ui := student.university_info) is not None:
        row += [
            (ui.program.code, formats.align_center),
            (ui.get_campus_display(), formats.align_center),
        ]
    else:
        row += [("", formats.align_center)] * 2

    if (ap := student.application_process) is not None:
        row += [
            (ap.mean_grade, formats.float),
            (int(ap.mean_grade * 10), formats.int),
            (ap.get_medical_examination_display(), formats.align_center),
            (ap.get_prof_psy_selection_display(), formats.align_center),
        ]

        for field in [
                "preferential_right", "characteristic_handed_over",
                "criminal_record_handed_over", "passport_handed_over",
                "registration_certificate_handed_over",
                "university_card_handed_over", "application_handed_over"
        ]:
            row.append(
                ("Да" if getattr(ap, field) else "Нет", formats.align_center))

        row += [
            (ap.pull_ups, formats.int),
            (ap.speed_run, formats.float),
            (ap.long_run, formats.float),
            (ap.physical_test_grade, formats.int),
        ]

    else:
        row += [("", formats.align_center)] * 14
        row += [(0, formats.align_center)]  # ФИЗО

    mean_grade_scaled = row[5][0]
    physical_test_grade = row[18][0]
    try:
        row += [(mean_grade_scaled + physical_test_grade, formats.int)]
    except TypeError:
        row += [(0, formats.int)]

    return row
