import uuid
from pathlib import Path

from django.db.models import QuerySet

import xlsxwriter

from common.utils.date import get_today_date_rus

from ams.models.applicants import Applicant

from ams.utils.export.formats import Formats


def generate_export(applicants: QuerySet, milspecialties: QuerySet) -> Path:
    """Generate an Excel file with information about the applicants
    using the competitive selection protocol template.

    Returns:
        A path to the generated Excel file.
    """

    path = Path(f"/tmp/{uuid.uuid4()}.xlsx")
    workbook = xlsxwriter.Workbook(path)
    formats = Formats.from_workbook(workbook)

    for milspecialty in milspecialties:
        worksheet = workbook.add_worksheet(milspecialty.code)
        _set_row_col_sizes(worksheet)
        _fill_header(
            worksheet=worksheet,
            formats=formats,
            milspecialty_code=milspecialty.code,
        )

        start = 15
        studs = applicants.filter(milspecialty=milspecialty)

        for row, applicant in enumerate(studs, start=start):  # Skip header
            cells = _make_applicant_row(
                applicant=applicant,
                formats=formats,
                index=row - start,  # applicant order number (from 0 to n)
            )

            for col, (data, cell_format) in enumerate(cells):
                worksheet.write(row, col, data, cell_format)

        # row = index of last element
        _fill_footer(
            worksheet=worksheet,
            formats=formats,
            start_row=start + len(studs),
            total_applicants=len(studs),
        )

    workbook.close()

    return path


def _set_row_col_sizes(worksheet: xlsxwriter.Workbook.worksheet_class,) -> None:
    worksheet.set_row(12, height=114)
    worksheet.set_row(13, height=114)
    # xlsxwriter has different dimensions for rows and cols
    # for some odd reason. All values here are gixen in pixels
    # (and then divided by 6)
    worksheet.set_column(0, 0, width=28 / 6)
    worksheet.set_column(1, 1, width=180 / 6)
    worksheet.set_column(2, 2, width=75 / 6)
    worksheet.set_column(3, 3, width=93 / 6)
    worksheet.set_column(4, 4, width=53 / 6)
    worksheet.set_column(5, 5, width=48 / 6)
    worksheet.set_column(6, 6, width=46 / 6)
    worksheet.set_column(7, 7, width=49 / 6)
    worksheet.set_column(8, 8, width=53 / 6)
    worksheet.set_column(9, 9, width=48 / 6)
    worksheet.set_column(10, 10, width=56 / 6)
    worksheet.set_column(11, 11, width=53 / 6)
    worksheet.set_column(12, 12, width=74 / 6)
    worksheet.set_column(13, 13, width=77 / 6)


def _fill_header(
    worksheet: xlsxwriter.Workbook.worksheet_class,
    formats: Formats,
    milspecialty_code: int,
) -> None:
    # Insert header
    worksheet.merge_range(
        "K1:N1",
        "УТВЕРЖДАЮ",
        formats.align_center,
    )
    worksheet.merge_range(
        "K2:N2",
        "Председатель конкурсной комиссии",
        formats.align_center,
    )
    worksheet.merge_range(
        "K3:M3",
        "полковник",
        formats.align_left,
    )
    worksheet.write(
        "N3",
        "А.Е. Усик",
        formats.align_center,
    )

    worksheet.merge_range(
        "K5:N5",
        get_today_date_rus(),
        formats.align_center,
    )

    worksheet.merge_range(
        "A7:N7",
        "ПРОТОКОЛ",
        formats.header,
    )
    worksheet.merge_range(
        "A8:N8",
        "конкурсного отбора граждан, изъявивших желание "
        "заключить договор об обучении по программе военной подготовки",
        formats.header,
    )
    worksheet.merge_range(
        "A9:N9",
        "офицеров (сержантов, солдат) запаса в военном учебном центре при",
        formats.header,
    )
    worksheet.merge_range(
        "A10:N10",
        "Национальном исследовательском университете "
        "\"Высшая школа экономики\"",
        formats.header,
    )
    worksheet.merge_range(
        "A11:N11",
        f"по военно-учетной специальности {milspecialty_code}",
        formats.header,
    )

    worksheet.merge_range(
        "A13:A14",
        "№ пп",
        formats.table_center,
    )
    worksheet.merge_range(
        "B13:C14",
        "Фамилия, имя, отчество,\n(дата рождения)",
        formats.table_center,
    )
    worksheet.merge_range(
        "D13:D14",
        "Код специальности (направление подготовки)",
        formats.table_center,
    )
    worksheet.merge_range(
        "E13:E14",
        "Результаты медицинского освидетельствования",
        formats.table_center_vertical,
    )
    worksheet.merge_range(
        "F13:F14",
        "Результаты профессионального психологического отбора",
        formats.table_center_vertical,
    )
    worksheet.merge_range(
        "G13:G14",
        "Преимущественное право",
        formats.table_center_vertical,
    )
    worksheet.merge_range(
        "H13:K13",
        "Результаты проверки уровня\nфизической подготовленности",
        formats.table_center,
    )
    worksheet.write("H14", "Сила", formats.table_center_vertical)
    worksheet.write("I14", "Скорость", formats.table_center_vertical)
    worksheet.write("J14", "Выносливость", formats.table_center_vertical)
    worksheet.write(
        "K14",
        "Результат по 100 бальной шкале",
        formats.table_center_vertical,
    )
    worksheet.merge_range(
        "L13:L14",
        "Оценка текущей успеваемости\n(по 100 бальной шкале)",
        formats.table_center_vertical,
    )
    worksheet.merge_range(
        "M13:M14",
        "Итоговый результат",
        formats.table_center,
    )
    worksheet.merge_range(
        "N13:N14",
        "Решение о допуске к военной подготовке в военном учебном центре",
        formats.table_center_vertical,
    )

    worksheet.write("A15", "1", formats.table_center)
    worksheet.merge_range("B15:C15", "2", formats.table_center)
    worksheet.write_row(14, 3, list(range(3, 14)), formats.table_center)


def _make_applicant_row(
    applicant: Applicant,
    formats: Formats,
    index: int,
) -> list[...]:
    row = [(f"{index+1}.", formats.table_center)]
    row += [(applicant.name.fullname, formats.table_name)]

    # pylint: disable=invalid-name
    if (bi := applicant.birth_info) is not None:
        row += [(bi.date, formats.table_date)]
    else:
        row += [("", formats.table_date)]

    if (ui := applicant.university_info) is not None:
        row += [(ui.program.code, formats.table_center)]
    else:
        row += [("", formats.table_center)]

    if (ap := applicant.application_process) is not None:
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

    physical_test_grade = row[10][0]
    mean_grade_scaled = row[11][0]
    try:
        row += [(physical_test_grade + mean_grade_scaled, formats.int)]
    except TypeError:
        row += [(0, formats.int)]

    row += [("", formats.table_center)]

    return row


def _fill_footer(
    worksheet: xlsxwriter.Workbook.worksheet_class,
    formats: Formats,
    start_row: int,
    total_applicants: int,
) -> None:
    row = start_row + 4  # 3 blank lines
    worksheet.merge_range(
        f"A{row}:N{row}",
        "2. Список граждан не допущенных к конкурсному отбору",
        formats.table_center)

    row = row + 4  # 3 blank lines
    lines = [
        ("Изъявили желание пройти обучение по программе военной подготовки -",
         f"{total_applicants} чел."),
        ("Допущены к военной подготовке -", "чел."),
        ("Не допущены к военной подготовке (не прошли по конкурсу) -", "чел."),
        ("Не допущены к конкурсному отбору -", "чел."),
    ]
    for line in lines:
        worksheet.merge_range(f"C{row}:H{row}", line[0], formats.align_left)
        worksheet.write(f"I{row}", line[1], formats.align_left)
        row += 1

    row = row + 3  # 3 blank lines (already had row += 1)
    worksheet.merge_range(f"D{row}:E{row}", "Члены комиссии:",
                          formats.align_left)
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

    worksheet.merge_range(f"D{row-1}:E{row-1}", "Секретарь комиссии:",
                          formats.align_left)
