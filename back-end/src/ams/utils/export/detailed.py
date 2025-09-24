import uuid
from pathlib import Path

from django.db.models import QuerySet

import xlsxwriter

from ams.models.applicants import Applicant

from ams.utils.export.formats import Formats


def _make_applicant_detail_row(
    applicant: Applicant, formats: Formats, index: int
) -> list[...]:
    row = [(f"{index + 1}.", formats.table_center)]
    row += [(applicant.fullname, formats.table_name)]

    if (uni_info := applicant.university_info) is not None:
        row += [
            (uni_info.program.faculty.title, formats.table_center),
            (uni_info.program.digit_code, formats.table_center),
            (uni_info.program.title, formats.table_center),
            (uni_info.group, formats.table_center),
            (uni_info.graduation_year, formats.table_center),
        ]
    else:
        row += [("", formats.table_center)] * 4

    # pylint: disable=invalid-name
    if (bi := applicant.birth_info) is not None:
        row += [
            (bi.date, formats.table_date),
            (f"{bi.country}, {bi.place}", formats.table_center),
        ]
    else:
        row += [("", formats.table_date)] * 2

    citizenship = applicant.citizenship or ""
    row += [(citizenship, formats.table_center)]

    nationality = applicant.nationality or ""
    row += [(nationality, formats.table_center)]

    marital_status = (
        applicant.get_marital_status_display() if applicant.marital_status else ""
    )
    row += [(marital_status, formats.table_center)]

    pa = applicant.permanent_address or ""
    row += [(pa, formats.table_center)]

    phone = applicant.contact_info.personal_phone_number or ""
    row += [(phone, formats.table_center)]

    tax_id = applicant.personal_documents_info.tax_id or ""
    row += [(tax_id, formats.table_center)]

    insurance_number = applicant.personal_documents_info.insurance_number or ""
    row += [(insurance_number, formats.table_center)]

    passport_series = applicant.passport.series or ""
    row += [(passport_series, formats.table_center)]

    passport_number = applicant.passport.code or ""
    row += [(passport_number, formats.table_center)]

    passport_ufms_name = applicant.passport.ufms_name or ""
    row += [(passport_ufms_name, formats.table_center)]

    passport_ufms_code = applicant.passport.ufms_code or ""
    row += [(passport_ufms_code, formats.table_center)]

    passport_issue_date = str(applicant.passport.issue_date) or ""
    row += [(passport_issue_date, formats.table_center)]

    ro = applicant.recruitment_office or ""
    row += [(ro, formats.table_center)]

    if fam := applicant.family.all():
        father = fam.filter(type="FA").first()
        mother = fam.filter(type="MO").first()
        brothers = list(fam.filter(type="BR").all())
        sisters = list(fam.filter(type="SI").all())
        row += (
            [
                (
                    f"{father.fullname}, "
                    f"{father.birth_info.date.strftime('%d.%m.%Y') + ',' if father.birth_info else ''} "
                    f"{father.permanent_address if father.permanent_address else ''}",
                    formats.align_left,
                )
            ]
            if father
            else [("", formats.align_left)]
        )
        row += (
            [
                (
                    f"{mother.fullname} "
                    f"{mother.birth_info.date.strftime('%d.%m.%Y') + ',' if mother.birth_info else ''} "
                    f"{mother.permanent_address if mother.permanent_address else ''}",
                    formats.align_left,
                )
            ]
            if mother
            else [("", formats.align_left)]
        )
        for bro in brothers:
            row += [
                (
                    f"{bro.fullname}, "
                    f"{bro.birth_info.date.strftime('%d.%m.%Y') + ',' if bro.birth_info else ''} "
                    f"{bro.permanent_address if bro.permanent_address else ''}",
                    formats.align_left,
                )
            ]
        for sis in sisters:
            row += [
                (
                    f"{sis.fullname}, "
                    f"{sis.birth_info.date.strftime('%d.%m.%Y') + ',' if sis.birth_info else ''} "
                    f"{sis.permanent_address if sis.permanent_address else ''}",
                    formats.align_left,
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
    formats.align_left.set_border()
    formats.align_left.set_align("vcenter")

    for milspecialty in milspecialties:
        worksheet = workbook.add_worksheet(milspecialty.code)
        set_col_size_details(worksheet)
        start = 2
        _fill_applicant_detail_header(worksheet=worksheet, formats=formats)
        studs = applicants.filter(milspecialty=milspecialty)
        max_cols = 0
        for row, applicant in enumerate(studs, start=start):  # Skip header
            cells = _make_applicant_detail_row(
                applicant=applicant,
                formats=formats,
                index=row - start,  # applicant order number (from 0 to n)
            )
            max_cols = max(max_cols, len(cells))
            for col, (data, cell_format) in enumerate(cells):
                worksheet.write(row, col, data, cell_format)
            if len(cells) < max_cols:
                for col in range(len(cells), max_cols):
                    worksheet.write(row, col, "", formats.align_left)
            worksheet.set_row(row, height=50)

    workbook.close()
    return path


def _fill_applicant_detail_header(
    worksheet: xlsxwriter.Workbook.worksheet_class,
    formats,
):
    row = (
        "№",
        "ФИО",
        "Название факультета",
        "Код специальности (направление подготовки)",
        "Название ОП",
        "Номер группы",
        "Год окончания ВУЗа",
        "Дата рождения",
        "Место рождения",
        "Гражданство",
        "Национальность",
        "Семейное положение",
        "Адрес прописки",
        "Номер телефона",
        "ИНН",
        "СНИЛС",
        "Паспорт_Серия",
        "Паспорт_Номер",
        "Паспорт_Выдан",
        "Паспорт_Код_Подразделения",
        "Паспорт_Дата_Выдачи",
        "Военкомат",
        "Отец",
        "Мать",
        "Братья/сестры",
    )
    worksheet.write_row(0, 0, row, formats.table_center)

    pasp_begin = 12
    pasp_end = 16

    # Объединение ячеек для столбца "Паспорт"
    worksheet.merge_range(0, pasp_begin, 0, pasp_end, "Паспорт", formats.table_center)

    # Запись "Серия", "Номер"... под объединенной ячейкой "Паспорт"
    passport_header = ("Серия", "Номер", "Выдан", "Код Подразделения", "Дата Выдачи")
    worksheet.write_row(1, pasp_begin, passport_header, formats.table_center)

    # Объединение ячеек для полей на две строки, кроме "Паспорт"
    for i in range(len(row)):
        if not (pasp_begin <= i <= pasp_end):
            worksheet.merge_range(0, i, 1, i, row[i], formats.table_center)


def set_col_size_details(worksheet: xlsxwriter.Workbook.worksheet_class):
    worksheet.set_column(0, 0, width=25 / 6)
    worksheet.set_column(1, 1, width=171 / 6)
    worksheet.set_column(2, 2, width=171 / 6)
    worksheet.set_column(3, 3, width=180 / 6)
    worksheet.set_column(4, 4, width=150 / 6)
    worksheet.set_column(5, 5, width=50 / 6)
    worksheet.set_column(6, 6, width=50 / 6)
    worksheet.set_column(7, 7, width=80 / 6)
    worksheet.set_column(8, 8, width=70 / 6)
    worksheet.set_column(9, 9, width=100 / 6)
    worksheet.set_column(10, 10, width=100 / 6)
    worksheet.set_column(11, 21, width=250 / 6)
