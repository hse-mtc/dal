import uuid
from pathlib import Path

from django.db.models import QuerySet

import xlsxwriter

from common.utils.date import get_today_date_rus

from ams.models.applicants import Applicant

from ams.utils.export.formats import Formats


def _make_applicant_detail_row(
        applicant: Applicant,
        formats: Formats,
        index: int
) -> list[...]:
    row = [(f"{index + 1}.", formats.table_center)]
    row += [(applicant.fullname, formats.table_name)]

    if (uni_info := applicant.university_info) is not None:
        row += [
            (uni_info.program.faculty.title, formats.table_center),
            (uni_info.program.title, formats.table_center),
            (uni_info.group, formats.table_center)
        ]
    else:
        row += [("", formats.table_center)] * 3

    # pylint: disable=invalid-name
    if (bi := applicant.birth_info) is not None:
        row += [
            (bi.date, formats.table_date),
            (f"{bi.country}, {bi.place}", formats.table_center)
        ]
    else:
        row += [("", formats.table_date)] * 2

    if (citizenship := applicant.citizenship) is not None:
        row += [(citizenship, formats.table_center)]
    else:
        row += [("", formats.table_center)]

    if (pa := applicant.permanent_address) is not None:
        row += [(pa, formats.table_center)]
    else:
        row += [("", formats.table_center)]

    if (ro := applicant.recruitment_office) is not None:
        row += [(ro, formats.table_center)]
    else:
        row += [("", formats.table_center)]

    if fam := applicant.family.all():
        fam = applicant.family.all()
        print(fam, len(fam))
        father = fam.filter(type="FA").first()
        mother = fam.filter(type="MO").first()
        brothers = list(fam.filter(type="BR").all())
        sisters = list(fam.filter(type="SI").all())
        row += [
            (
                f"{father.fullname}, {father.birth_info.date + ',' if father.birth_info else ''} "
                f"{father.permanent_address if father.permanent_address else ''}",
                formats.align_left
            )
        ] if father else [("", formats.align_left)]
        row += [
            (
                f"{mother.fullname} {mother.birth_info.date + ',' if mother.birth_info else ''} "
                f"{mother.permanent_address if mother.permanent_address else ''}",
                formats.align_left
            )
        ] if mother else [("", formats.align_left)]
        for bro in brothers:
            row += [
                (
                    f"{bro.fullname}, {bro.birth_info.date + ',' if bro.birth_info else ''} "
                    f"{bro.permanent_address if bro.permanent_address else ''}",
                    formats.align_left
                )
            ]
        for sis in sisters:
            row += [
                (
                    f"{sis.fullname}, {sis.birth_info.date + ',' if sis.birth_info else ''} "
                    f"{sis.permanent_address if sis.permanent_address else ''}",
                    formats.align_left
                )
            ]
    else:
        row += [("", formats.align_left)] * 3

    return row


def generate_applicants_detail(applicants: QuerySet, milspecialties: QuerySet) -> Path:
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
        start = 1
        _fill_applicant_detail_header(
            worksheet=worksheet,
            formats=formats
        )
        studs = applicants.filter(milspecialty=milspecialty)
        for row, applicant in enumerate(studs, start=start):  # Skip header
            cells = _make_applicant_detail_row(
                applicant=applicant,
                formats=formats,
                index=row - start,  # applicant order number (from 0 to n)
            )

            for col, (data, cell_format) in enumerate(cells):
                worksheet.write(row, col, data, cell_format)
            worksheet.set_row(row, height=50)

    workbook.close()
    return path


def _fill_applicant_detail_header(
        worksheet: xlsxwriter.Workbook.worksheet_class,
        formats,
):
    row = (
        "№", "ФИО", "Название факультета", "Название ОП", "Номер группы",
        "Дата рождения", "Место рождения", "Гражданство",
        "Адрес прописки", "Военкомат", "Отец", "Мать", "Братья/сестры"
    )
    worksheet.write_row(0, 0, row, formats.table_center)


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
            worksheet.set_row(row, height=50)

        # row = index of last element
        _fill_footer(
            worksheet=worksheet,
            formats=formats,
            start_row=start + len(studs),
            total_applicants=len(studs),
        )

    workbook.close()

    return path


def _set_row_col_sizes(
    worksheet: xlsxwriter.Workbook.worksheet_class,
) -> None:
    worksheet.set_row(12, height=130)
    worksheet.set_row(13, height=130)
    # xlsxwriter has different dimensions for rows and cols
    # for some odd reason. All values here are gixen in pixels
    # (and then divided by 6)
    worksheet.set_column(0, 0, width=51 / 6)
    worksheet.set_column(1, 1, width=171 / 6)
    worksheet.set_column(2, 2, width=94 / 6)
    worksheet.set_column(3, 3, width=92 / 6)
    worksheet.set_column(4, 4, width=177 / 6)
    worksheet.set_column(5, 5, width=43 / 6)
    worksheet.set_column(6, 6, width=48 / 6)
    worksheet.set_column(7, 7, width=46 / 6)
    worksheet.set_column(8, 8, width=49 / 6)
    worksheet.set_column(9, 9, width=53 / 6)
    worksheet.set_column(10, 10, width=48 / 6)
    worksheet.set_column(11, 11, width=56 / 6)
    worksheet.set_column(12, 12, width=53 / 6)
    worksheet.set_column(13, 13, width=74 / 6)
    worksheet.set_column(14, 14, width=77 / 6)


def _fill_header(
    worksheet: xlsxwriter.Workbook.worksheet_class,
    formats: Formats,
    milspecialty_code: int,
) -> None:
    # Insert header
    worksheet.merge_range(
        "L1:O1",
        "УТВЕРЖДАЮ",
        formats.align_center,
    )
    worksheet.merge_range(
        "L2:O2",
        "Председатель конкурсной комиссии",
        formats.align_center,
    )
    worksheet.merge_range(
        "L3:N3",
        "полковник",
        formats.align_left,
    )
    worksheet.write(
        "O3",
        "А.Е. Усик",
        formats.align_center,
    )

    worksheet.merge_range(
        "L5:O5",
        get_today_date_rus(),
        formats.align_center,
    )

    worksheet.merge_range(
        "A7:O7",
        "ПРОТОКОЛ",
        formats.header,
    )
    worksheet.merge_range(
        "A8:O8",
        "конкурсного отбора граждан, изъявивших желание "
        "заключить договор об обучении по программе военной подготовки",
        formats.header,
    )
    worksheet.merge_range(
        "A9:O9",
        "офицеров (сержантов, солдат) запаса в военном учебном центре при",
        formats.header,
    )
    worksheet.merge_range(
        "A10:O10",
        "Национальном исследовательском университете " '"Высшая школа экономики"',
        formats.header,
    )
    worksheet.merge_range(
        "A11:O11",
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
        "Наименование программы",
        formats.table_center,
    )
    worksheet.merge_range(
        "F13:F14",
        "Результаты медицинского освидетельствования",
        formats.table_center_vertical,
    )
    worksheet.merge_range(
        "G13:G14",
        "Результаты профессионального психологического отбора",
        formats.table_center_vertical,
    )
    worksheet.merge_range(
        "H13:H14",
        "Преимущественное право",
        formats.table_center_vertical,
    )
    worksheet.merge_range(
        "I13:L13",
        "Результаты проверки уровня\nфизической подготовленности",
        formats.table_center,
    )
    worksheet.write("I14", "Сила", formats.table_center_vertical)
    worksheet.write("J14", "Скорость", formats.table_center_vertical)
    worksheet.write("K14", "Выносливость", formats.table_center_vertical)
    worksheet.write(
        "L14",
        "Результат по 100 бальной шкале",
        formats.table_center_vertical,
    )
    worksheet.merge_range(
        "M13:M14",
        "Оценка текущей успеваемости\n(по 100 бальной шкале)",
        formats.table_center_vertical,
    )
    worksheet.merge_range(
        "N13:N14",
        "Итоговый результат",
        formats.table_center,
    )
    worksheet.merge_range(
        "O13:O14",
        "Решение о допуске к военной подготовке в военном учебном центре",
        formats.table_center_vertical,
    )

    worksheet.write("A15", "1", formats.table_center)
    worksheet.merge_range("B15:C15", "2", formats.table_center)
    worksheet.write_row(14, 3, list(range(3, 15)), formats.table_center)


def _make_applicant_row(
    applicant: Applicant,
    formats: Formats,
    index: int,
) -> list[...]:
    row = [(f"{index+1}.", formats.table_center)]
    row += [(applicant.fullname, formats.table_name)]

    # pylint: disable=invalid-name
    if (bi := applicant.birth_info) is not None:
        row += [(bi.date, formats.table_date)]
    else:
        row += [("", formats.table_date)]

    if (ui := applicant.university_info) is not None:
        row += [(ui.program.digit_code, formats.table_center)]
        row += [(ui.program.title, formats.table_center)]
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
        f"A{row}:O{row}",
        "2. Список граждан не допущенных к конкурсному отбору",
        formats.table_center,
    )

    row = row + 4  # 3 blank lines
    lines = [
        (
            "Изъявили желание пройти обучение по программе военной подготовки -",
            f"{total_applicants} чел.",
        ),
        ("Допущены к военной подготовке -", "чел."),
        ("Не допущены к военной подготовке (не прошли по конкурсу) -", "чел."),
        ("Не допущены к конкурсному отбору -", "чел."),
    ]
    for line in lines:
        worksheet.merge_range(f"C{row}:H{row}", line[0], formats.align_left)
        worksheet.write(f"I{row}", line[1], formats.align_left)
        row += 1

    row = row + 3  # 3 blank lines (already had row += 1)
    worksheet.merge_range(f"D{row}:E{row}", "Члены комиссии:", formats.align_left)
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

    worksheet.merge_range(
        f"D{row-1}:E{row-1}", "Секретарь комиссии:", formats.align_left
    )
