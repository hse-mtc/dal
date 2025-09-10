from pathlib import Path
from tempfile import NamedTemporaryFile
from datetime import date
from openpyxl import Workbook

from lms.models.students import Student

HEADERS = [
    "ФГОО ВО в котором обучается студент",
    "ФГОО ВО при которой создан ВУЦ",
    "ВУС",
    "ОВУ",
    "ФГОС",
    "Программа военной подготовки",
    "Год зачисления в ВУЗ",
    "Год начала обучения в ВУЦ",
    "Месяц начала обучения в ВУЦ",
    "Срок обучения (месяцев)",
    "Год окончания ВУЦ",
    "Месяц окончания обучения в ВУЦ",
    "Отметка о завершении военной подготовки",
    "Год окончания ВУЗа",
    "Месяц окончания обучения в ВУЗе",
    "Личный номер",
    "Фамилия",
    "Имя",
    "Отчество",
    "Дата рождения",
    "Место рождения",
    "Националь-ность",
    "Пол",
    "СНИЛС",
    "ИНН",
    "Паспортные данные",
    "Адрес регистрации",
    "Номер телефона",
    "Семейное положение",
    "Кол-во детей",
    "Военный комиссариат (по месту жительства)",
    "Военный комиссариат (в который будет направлено личное дело)",
    "Служба ВС РФ (периоды)",
    "Примечание",
    "Статус",
    "Приказ о зачислении",
    "Приказ о отчислении",
    "Причина отчисления",
]


def _fmt_date(d: date | None) -> str:
    return d.strftime("%d.%m.%Y") if isinstance(d, date) else ""


def _passport_str(st: Student) -> str:
    ps = st.passport
    if not ps:
        return ""
    parts = []
    if getattr(ps, "series", None):
        parts.append(f"серия: {ps.series}")
    if getattr(ps, "code", None):
        parts.append(f"номер: {ps.code}")
    if getattr(ps, "ufms_name", None):
        parts.append(f"выдан: {ps.ufms_name}")
    if getattr(ps, "issue_date", None):
        parts.append(f"дата выдачи: {_fmt_date(ps.issue_date)}")
    if getattr(ps, "ufms_code", None):
        parts.append(f"код подразделения: {ps.ufms_code}")
    return ", ".join(parts)


def generate_export(students_qs, _milspecialties_qs) -> Path:
    """
    Экспорт студентов в Excel файл.

    Многие поля отсутствуют в текущей модели Student и оставлены пустыми.
    При необходимости их можно добавить в модель или получить из других источников.
    """
    wb = Workbook(write_only=True)
    ws = wb.create_sheet(title="НИУ ВШЭ офицеры запаса")
    default = wb.worksheets[0]
    if default.title != ws.title and len(default._cells) == 0:
        wb.remove(default)
    ws.append(HEADERS)

    for st in students_qs:
        ui = st.university_info
        bi = st.birth_info
        ci = st.contact_info
        pdi = st.personal_documents_info
        mg = st.milgroup

        fgou = (
            ui.program.faculty.title if ui and ui.program and ui.program.faculty else ""
        )

        fgou_vuc = mg.milfaculty.title if mg and mg.milfaculty else ""

        vus = mg.milspecialty.code if mg and mg.milspecialty else ""

        ovu = mg.title if mg else ""

        fgos = ui.program.code if ui and ui.program else ""

        mil_prog = mg.milspecialty.title if mg and mg.milspecialty else ""

        vuc_start_year = ""
        vuc_start_month = ""
        vuc_duration_months = ""
        vuc_end_year = ""
        vuc_end_month = ""
        mil_completed = ""
        grad_year = ""
        grad_month = ""
        enrollment_order = ""
        expel_order = ""
        expel_reason = ""
        vk_destination = ""
        personal_number = str(st.id)
        surname = st.surname
        name = st.name
        patronymic = st.patronymic or ""
        birth_date = _fmt_date(bi.date if bi else None)
        birth_place = bi.place if bi else ""
        nationality = st.citizenship or ""
        gender = "мужской"
        snils = pdi.insurance_number if pdi else ""
        inn = pdi.tax_id if pdi else ""
        passport_line = _passport_str(st)
        address = st.permanent_address or ""
        phone = ci.personal_phone_number if ci else ""
        # Поля, которых нет в модели
        marital_status = ""  # Нет в модели
        children_count = ""  # Нет в модели

        # Военкомат
        vk_home = st.recruitment_office or ""
        service_periods = ""  # Нет в модели
        note = ""  # Нет в модели
        # Статус студента
        status = (
            st.get_status_display() if hasattr(st, "get_status_display") else st.status
        )

        row = [
            fgou,
            fgou_vuc,
            vus,
            ovu,
            fgos,
            mil_prog,
            year_enrolled,
            vuc_start_year,
            vuc_start_month,
            vuc_duration_months,
            vuc_end_year,
            vuc_end_month,
            mil_completed,
            grad_year,
            grad_month,
            personal_number,
            surname,
            name,
            patronymic,
            birth_date,
            birth_place,
            nationality,
            gender,
            snils,
            inn,
            passport_line,
            address,
            phone,
            marital_status,
            children_count,
            vk_home,
            vk_destination,
            service_periods,
            note,
            status,
            enrollment_order,
            expel_order,
            expel_reason,
        ]
        ws.append(row)

    tmp = NamedTemporaryFile(delete=False, suffix=".xlsx")
    wb.save(tmp.name)
    return Path(tmp.name)
