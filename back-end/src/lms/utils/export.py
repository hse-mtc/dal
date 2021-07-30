import uuid

from dataclasses import dataclass
from pathlib import Path
from datetime import datetime

from django.db.models import QuerySet

import xlsxwriter

from xlsxwriter.format import Format
from xlsxwriter.workbook import Workbook

from lms.models.students import Student
from lms.functions import get_today_date_rus


@dataclass
class Formats:
    header: Format
    align_center: Format
    align_left: Format
    russian_date: Format
    int: Format
    float: Format
    underline: Format
    table_center: Format
    table_center_vertical: Format
    table_name: Format
    table_date: Format

    @classmethod
    def from_workbook(cls, workbook: Workbook) -> "Formats":
        return Formats(
            header=workbook.add_format({
                "font_name": "Times New Roman",
                "font_size": 12,
                "bold": True,
                "align": "center"
            }),
            align_center=workbook.add_format({
                "font_name": "Times New Roman",
                "font_size": 12,
                "align": "center"
            }),
            align_left=workbook.add_format({
                "font_name": "Times New Roman",
                "font_size": 12,
                "align": "left"
            }),
            russian_date=workbook.add_format({
                "font_name": "Times New Roman",
                "font_size": 12,
                "num_format": "dd.mm.yyyy",
                "border": 1,
                "align": "center",
                "valign": "vcenter",
            }),
            int=workbook.add_format({
                "font_name": "Times New Roman",
                "font_size": 12,
                "align": "center",
                "valign": "vcenter",
                "border": 1,
                "num_format": "#0"
            }),
            float=workbook.add_format({
                "font_name": "times new roman",
                "font_size": 12,
                "align": "center",
                "valign": "vcenter",
                "border": 1,
                "num_format": "#,##0.00"
            }),
            underline=workbook.add_format({
                "font_name": "times new roman",
                "font_size": 12,
                "align": "left",
                "valign": "vcenter",
                "bottom": 1,
            }),
            table_center=workbook.add_format({
                "font_name": "Times New Roman",
                "font_size": 12,
                "align": "center",
                "valign": "vcenter",
                "border": 1,
                "text_wrap": True,
            }),
            table_center_vertical=workbook.add_format({
                "font_name": "Times New Roman",
                "font_size": 12,
                "align": "center",
                "valign": "vcenter",
                "border": 1,
                "text_wrap": True,
                "rotation": 90,
            }),
            table_name=workbook.add_format({
                "font_name": "Times New Roman",
                "font_size": 12,
                "align": "center",
                "valign": "vcenter",
                "left": 1,
                "top": 1,
                "bottom": 1,
                "text_wrap": True,
            }),
            table_date=workbook.add_format({
                "font_name": "Times New Roman",
                "font_size": 12,
                "align": "center",
                "valign": "vcenter",
                "right": 1,
                "top": 1,
                "bottom": 1,
                "text_wrap": True,
                "num_format": "dd.mm.yyyy",
            }),
        )


def generate_default_export(students: QuerySet, milspecialties: QuerySet) -> Path:
    """Generate an Excel file with information about the students.

    Returns:
        A path to the generated Excel file.
    """

    path = Path(f"/tmp/{uuid.uuid4()}.xlsx")
    workbook = xlsxwriter.Workbook(path)
    formats = Formats.from_workbook(workbook)

    for milspecialty in milspecialties:
        worksheet = workbook.add_worksheet(milspecialty.code)
        _fill_default_header(worksheet=worksheet,
                             cell_format=formats.table_center)

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


def generate_comp_sel_protocol_export(students: QuerySet, milspecialties: QuerySet) -> Path:
    """Generate an Excel file with information about the students
    using the competitive selection protocol template.

    Returns:
        A path to the generated Excel file.
    """

    path = Path(f"/tmp/{uuid.uuid4()}.xlsx")
    workbook = xlsxwriter.Workbook(path)
    formats = Formats.from_workbook(workbook)

    for milspecialty in milspecialties:
        worksheet = workbook.add_worksheet(milspecialty.code)
        _fill_comp_sel_protocol_header(
            worksheet=worksheet,
            formats=formats,
            milspecialty_code=milspecialty.code,
        )

        start = 15
        studs = students.filter(milspecialty=milspecialty)

        for row, student in enumerate(studs, start=start):  # Skip header
            cells = _make_student_comp_sel_protocol_row(
                student=student,
                formats=formats,
                index=row-start,  # student order number (from 0 to n)
            )

            for col, (data, cell_format) in enumerate(cells):
                worksheet.write(row, col, data, cell_format)

        # row = index of last element
        _fill_comp_sel_protocol_footer(
            worksheet=worksheet,
            formats=formats,
            start_row=start+len(studs),
        )

    workbook.close()
    return path


def _fill_default_header(
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


def _fill_comp_sel_protocol_header(
    worksheet: xlsxwriter.Workbook.worksheet_class,
    formats: Formats,
    milspecialty_code: int,
) -> None:
    # Insert header
    worksheet.merge_range("K1:N1", "УТВЕРЖДАЮ", formats.align_center)
    worksheet.merge_range(
        "K2:N2", "Председатель конкурсной комиссии", formats.align_center)
    worksheet.merge_range("K3:M3", "полковник", formats.align_left)
    worksheet.write("N3", "А.Е. Усик", formats.align_center)

    worksheet.merge_range("K5:N5", get_today_date_rus(), formats.align_center)

    worksheet.merge_range("A7:N7", "ПРОТОКОЛ", formats.header)
    worksheet.merge_range("A8:N8", "конкурсного отбора граждан, изъявивших желание "
                          "заключить договор об обучении по программе военной подготовки", formats.header)
    worksheet.merge_range(
        "A9:N9", "офицеров (сержантов, солдат) запаса в военном учебном центре при", formats.header)
    worksheet.merge_range(
        "A10:N10", "Национальном исследовательском университете \"Высшая школа экономики\"", formats.header)
    worksheet.merge_range(
        "A11:N11", f"по военно-учетной специальности {milspecialty_code}", formats.header)

    worksheet.merge_range("A13:A14", "№ пп", formats.table_center)
    worksheet.merge_range(
        "B13:C14", "Фамилия, имя, отчество,\n(дата рождения)", formats.table_center)
    worksheet.merge_range(
        "D13:D14", "Код специальности (направление подготовки)", formats.table_center)
    worksheet.merge_range(
        "E13:E14", "Результаты медицинского освидетельствования", formats.table_center_vertical)
    worksheet.merge_range(
        "F13:F14", "Результаты профессионального психологического отбора", formats.table_center_vertical)
    worksheet.merge_range(
        "G13:G14", "Преимущественное право", formats.table_center_vertical)
    worksheet.merge_range(
        "H13:K13", "Результаты проверки уровня\nфизической подготовленности", formats.table_center)
    worksheet.write("H14", "Сила", formats.table_center_vertical)
    worksheet.write("I14", "Скорость", formats.table_center_vertical)
    worksheet.write("J14", "Выносливость", formats.table_center_vertical)
    worksheet.write("K14", "Результат по 100 бальной шкале",
                    formats.table_center_vertical)
    worksheet.merge_range(
        "L13:L14", "Оценка текущей успеваемости\n(по 100 бальной шкале)", formats.table_center_vertical)
    worksheet.merge_range("M13:M14", "Итоговый результат",
                          formats.table_center)
    worksheet.merge_range(
        "N13:N14", "Решение о допуске к военной подготовке в военном учебном центре", formats.table_center_vertical)

    worksheet.write("A15", "1", formats.table_center)
    worksheet.merge_range("B15:C15", "2", formats.table_center)
    worksheet.write_row(14, 3, list(range(3, 14)), formats.table_center)

    # Setup column and row lengths
    worksheet.set_row(12, height=114)
    worksheet.set_row(13, height=114)
    worksheet.set_column(0, 0, width=28/6)
    worksheet.set_column(1, 1, width=180/6)
    worksheet.set_column(2, 2, width=75/6)
    worksheet.set_column(3, 3, width=93/6)
    worksheet.set_column(4, 4, width=53/6)
    worksheet.set_column(5, 5, width=48/6)
    worksheet.set_column(6, 6, width=46/6)
    worksheet.set_column(7, 7, width=49/6)
    worksheet.set_column(8, 8, width=53/6)
    worksheet.set_column(9, 9, width=48/6)
    worksheet.set_column(10, 10, width=56/6)
    worksheet.set_column(11, 11, width=53/6)
    worksheet.set_column(12, 12, width=74/6)
    worksheet.set_column(13, 13, width=77/6)


def _make_student_row(
    student: Student,
    formats: Formats,
) -> list[...]:
    row = [(student.full_name, formats.table_center)]

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


def _make_student_comp_sel_protocol_row(
    student: Student,
    formats: Formats,
    index: int,
) -> list[...]:
    row = [(f"{index+1}.", formats.table_center)]
    row += [(student.full_name, formats.table_name)]

    if (bi := student.birth_info) is not None:
        row += [(bi.date, formats.table_date)]
    else:
        row += [("", formats.table_date)]

    if (ui := student.university_info) is not None:
        row += [(ui.program.code, formats.table_center)]
    else:
        row += [("", formats.table_center)]

    if (ap := student.application_process) is not None:
        row += [
            (ap.get_medical_examination_display(), formats.table_center),
            (ap.get_prof_psy_selection_display(), formats.table_center),
        ]
        row += [("Да" if ap.preferential_right else "Нет", formats.table_center)]

        row += [
            (ap.pull_ups, formats.int),
            (ap.speed_run, formats.float),
            (ap.long_run, formats.float),
            (ap.physical_test_grade, formats.int),
        ]

        row += [(int(ap.mean_grade * 10), formats.int)]

    else:
        row += [("", formats.table_center)] * 6
        row += [(0, formats.table_center)] * 2  # ФИЗО + Ср Оценка

    mean_grade_scaled = row[9][0]
    physical_test_grade = row[10][0]
    try:
        row += [(mean_grade_scaled + physical_test_grade, formats.int)]
    except TypeError:
        row += [(0, formats.int)]

    row += [("", formats.table_center)]

    return row


def _fill_comp_sel_protocol_footer(
    worksheet: xlsxwriter.Workbook.worksheet_class,
    formats: Formats,
    start_row: int,
) -> None:
    row = start_row + 4  # 3 blank lines
    worksheet.merge_range(
        f"A{row}:N{row}", "2. Список граждан не допущенных к конкурсному отбору", formats.table_center)

    row = row + 4  # 3 blank lines
    lines = [
        "Изъявили желание пройти обучение по программе военной подготовки -",
        "Допущены к военной подготовке -",
        "Не допущены к военной подготовке (не прошли по конкурсу) -",
        "Не допущены к конкурсному отбору -",
    ]
    for line in lines:
        worksheet.merge_range(f"C{row}:H{row}", line, formats.align_left)
        worksheet.write(f"I{row}", "чел.", formats.align_left)
        row += 1

    row = row + 3  # 3 blank lines (already had row += 1)
    worksheet.merge_range(
        f"D{row}:E{row}", "Члены комиссии:", formats.align_left)
    lines = [
        ("подполковник", ""),
        ("подполковник", "М.И. Гвозд"),
        ("подполковник", ""),
        ("", "Е.К. Артемов"),
        ("", "О.С. Булыкин"),
        ("полковник", "В.А. Коргутов"),
        ("полковник", "А.В. Кашин"),
    ]
    for line in lines:
        worksheet.merge_range(f"F{row}:G{row}", line[0], formats.underline)
        worksheet.write(f"H{row}", "", formats.underline)
        worksheet.write(f"I{row}", "", formats.underline)
        worksheet.write(f"J{row}", "", formats.underline)
        worksheet.merge_range(f"K{row}:L{row}", line[1], formats.underline)
        row += 1

    worksheet.merge_range(f"D{row-1}:E{row-1}",
                          "Секретарь комиссии:", formats.align_left)
