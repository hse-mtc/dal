import uuid
from pathlib import Path

from django.db.models import QuerySet

import xlsxwriter

from ams.models.applicants import Applicant

from ams.utils.export.formats import Formats
from common.models.universities import Program


def generate_export(applicants: QuerySet, milspecialties: QuerySet) -> Path:
    """Generate an Excel file with information about the applicants.

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

        for row, applicant in enumerate(
            applicants.filter(milspecialty=milspecialty),
            start=1,  # Skip header.
        ):
            cells = _make_applicant_row(
                applicant=applicant,
                formats=formats,
            )
            for col, (data, cell_format) in enumerate(cells):
                worksheet.write(row, col, data, cell_format)

    workbook.close()
    return path


def _set_row_col_sizes(
    worksheet: xlsxwriter.Workbook.worksheet_class,
) -> None:
    worksheet.set_column(0, 0, 30)  # ФИО
    worksheet.set_column(1, 1, 15)  # Дата рождения
    worksheet.set_column(2, 2, 30)  # Код специальности
    worksheet.set_column(3, 3, 45)  # Направление специальности
    worksheet.set_column(6, 6, 15)  # Кампус
    worksheet.set_column(6, 6, 13)  # Средний балл / 100
    worksheet.set_column(7, 7, 34)  # РМО
    worksheet.set_default_row(30) # Высота строки
    worksheet.set_row(0, 40) # Заголовок


def _fill_header(
    worksheet: xlsxwriter.Workbook.worksheet_class,
    cell_format: xlsxwriter.workbook.Format,
) -> None:
    columns = [
        "ФИО",
        "Дата рождения",
        "Код специальности (направление подготовки)",
        "Наименование программы",
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


def _make_applicant_row(
    applicant: Applicant,
    formats: Formats,
) -> list[...]:
    row = [(applicant.fullname, formats.table_center)]

    # pylint: disable=invalid-name
    if (bi := applicant.birth_info) is not None:
        row += [(bi.date, formats.russian_date)]
    else:
        row += [("", formats.table_center)]

    if (ui := applicant.university_info) is not None:
        row += [
            (ui.program.digit_code, formats.table_center),
            (ui.program.title, formats.table_center),
            (ui.program.faculty.get_campus_display(), formats.table_center),
        ]
    else:
        row += [("", formats.table_center)] * 2

    if (ap := applicant.application_process) is not None:
        row += [
            (ap.mean_grade, formats.float),
            (int(ap.mean_grade * 10), formats.int),
            (ap.get_medical_examination_display(), formats.table_center),
            (ap.get_prof_psy_selection_display(), formats.table_center),
        ]

        for field in [
            "preferential_right",
            "characteristic_handed_over",
            "criminal_record_handed_over",
            "passport_handed_over",
            "registration_certificate_handed_over",
            "university_card_handed_over",
            "application_handed_over",
        ]:
            row.append(("Да" if getattr(ap, field) else "Нет", formats.table_center))

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
