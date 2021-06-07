import uuid

from pathlib import Path

from django.db.models import QuerySet

import xlsxwriter

from lms.models.students import Student


def generate_excel(students: QuerySet, milspecialties: QuerySet) -> Path:
    """Generate an Excel file with information about the students.

    Returns:
        A path to the generated Excel file.
    """

    path = Path(f"/tmp/{uuid.uuid4()}.xlsx")
    workbook = xlsxwriter.Workbook(path)

    # define formats
    header_format = workbook.add_format({"bold": True, "align": "center"})
    align_center = workbook.add_format({"align": "center"})
    russian_date = workbook.add_format({
        "num_format": "dd.mm.yyyy",
        "align": "center",
    })
    mean_grade = workbook.add_format({
        "align": "center",
        "num_format": "#,##0.00"
    })

    for milspecialty in milspecialties:
        worksheet = workbook.add_worksheet(milspecialty.code)
        _fill_header(worksheet=worksheet, cell_format=header_format)

        for row, student in enumerate(
                students.filter(milspecialty=milspecialty),
                start=1,  # Skip header.
        ):
            cells = _make_student_row(
                student=student,
                align_center=align_center,
                russian_date=russian_date,
                mean_grade=mean_grade,
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
        "РМО",
        "РППО",
        "ПП",
        "Хар-ка",
        "СН",
        "Паспорт",
        "ПС",
        "СБ",
        "Заявление",
    ]

    worksheet.write_row(0, 0, columns)
    worksheet.set_row(0, cell_format=cell_format)
    worksheet.set_column(0, 0, 30)  # ФИО
    worksheet.set_column(1, 1, 15)  # Дата рождения
    worksheet.set_column(3, 3, 15)  # Кампус
    worksheet.set_column(5, 5, 34)  # РМО


def _make_student_row(
    student: Student,
    align_center: xlsxwriter.workbook.Format,
    russian_date: xlsxwriter.workbook.Format,
    mean_grade: xlsxwriter.workbook.Format,
) -> list[...]:
    row = [(student.full_name, align_center)]

    if student.birth_info is not None:
        row.append((student.birth_info.date, russian_date))
    else:
        row.append(("", align_center))

    if student.university_info is not None:
        row += [
            (student.university_info.program.code, align_center),
            (student.university_info.get_campus_display(), align_center),
        ]
    else:
        row += [("", align_center)] * 2

    if student.application_process is not None:
        row += [
            (student.application_process.mean_grade, mean_grade),
            (student.application_process.get_medical_examination_display(),
             align_center),
            (student.application_process.get_prof_psy_selection_display(),
             align_center),
        ]
        for field in [
                "preferential_right", "characteristic_handed_over",
                "criminal_record_handed_over", "passport_handed_over",
                "registration_certificate_handed_over",
                "university_card_handed_over", "application_handed_over"
        ]:
            row.append(
                ("Да" if getattr(student.application_process, field) else "Нет",
                 align_center))
    else:
        row += [("", align_center)] * 9

    return row
