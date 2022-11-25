import base64
import logging as log

import jinja2

import shutil

from docxtpl import DocxTemplate

from auth import obtain_credentials
from email_service import EmailService
from drive import DriveService
from campuses import Campus
from family import RelativeType
from proto import Applicant
from config import (
    TEMPLATES_DIR,
    GENERATED_DIR,
    EMAIL_HOST,
    EMAIL_PORT,
    EMAIL_HOST_USER,
    EMAIL_HOST_PASSWORD,
    EMAIL_USE_TLS,
)

from email_utils import create_message
from date_utils import (
    date_to_russian_format,
    month_to_russian_title,
    today,
)

WATCHDOC_FOLDER: str = "watchdoc"
APPLICANTS_FOLDER: str = "Абитуриенты"
CAMPUSES_FOLDER: str = "Кампусы"

DUMMY_IMAGE = TEMPLATES_DIR / "dummy.png"

DOCUMENTS = [
    ("mec-application.docx", "Заявление на поступление.docx"),
    ("ro-reference.docx", "Направление ВК.docx"),
    ("ro-reference-signed.docx", "Направление ВК (подписано).docx"),
    ("medical-records.docx", "Медкарта.docx"),
    ("family-info.docx", "Сведения о семье.docx"),
    ("applicant-form.docx", "Анкета абитуриента.docx"),
]


class WatchDocService:
    """WatchDoc manages applicants' documents.

    Usage:
        wds = WatchDocService()
        wds.generate_documents(applicant)
        folder_link = wds.upload_documents(applicant)
        wds.notify(applicant, folder_link)
    """
    def generate_documents(self, applicant: Applicant, docs=DOCUMENTS):
        applicant_path = applicant.full_name + ' ' +\
            applicant.contact_info.corporate_email
        applicant_dir = GENERATED_DIR / applicant_path

        if applicant_dir.exists():
            shutil.rmtree(applicant_dir, ignore_errors=True)
        applicant_dir.mkdir(exist_ok=True)

        parents = [
            r for r in applicant.family
            if r.type in [RelativeType.FATHER, RelativeType.MOTHER]
        ]
        siblings = [
            r for r in applicant.family
            if r.type in [RelativeType.BROTHER, RelativeType.SISTER]
        ]

        data = applicant.dict()

        photo = data.pop("photo")
        photo_path = applicant_dir / "photo"
        with open(photo_path, "wb") as f:
            f.write(base64.b64decode(photo.encode()))

        context = {
            "date": today(),
            "full_name": applicant.full_name,
            "parents": parents,
            "siblings": siblings,
            **data,
        }

        for (en, rus) in docs:
            doc = DocxTemplate(TEMPLATES_DIR / en)
            doc.render(context, self.jinja_env)
            doc.replace_media(DUMMY_IMAGE, photo_path)
            doc.save(applicant_dir / rus)



    def upload_documents(self, applicant: Applicant):
        email = applicant.contact_info.corporate_email
        campus = applicant.university_info.campus.value
        folder_name = f"{applicant.full_name} {email}"

        applicant_folder = self.ds.obtain_folder(
            name=folder_name,
            parents=[self._campus_folders[campus]["id"]],
            delete_if_exists=True
        )

        for (_, rus) in DOCUMENTS:
            body = {
                "name": rus,
                "parents": [applicant_folder["id"]],
            }
            self.ds.upload_docx(
                body=body,
                path=GENERATED_DIR / email / rus,
            )

        self.ds.read_share_folder_with_anyone(
            folder_id=applicant_folder["id"],
        )

        return applicant_folder["webViewLink"]

    def notify(self, applicant: Applicant, folder_link: str):
        email = applicant.contact_info.corporate_email
        msg = create_message(to=email, link=folder_link)
        self.email_service.send_message(email, body=msg)

    # --------------------------------------------------------------------------
    # Internal methods

    def __init__(self) -> None:
        # Templates
        self.jinja_env = self._init_jinja_env()

        # Credentials
        # credentials = obtain_credentials()

        # Email
        self.email_service = EmailService(
            EMAIL_HOST,
            EMAIL_PORT,
            EMAIL_HOST_USER,
            EMAIL_HOST_PASSWORD,
            EMAIL_USE_TLS
        )

        # Drive
        # self.ds = DriveService(credentials)
        # self._watchdoc_folder = self._init_watchdoc_folder()
        # self._applicants_folder = self._init_applicants_folder()
        # self._campuses_folder = self._init_campuses_folder()
        # self._campus_folders = self._init_campus_folders()

    def _init_jinja_env(self):
        env = jinja2.Environment()
        env.filters["date_to_russian_format"] = date_to_russian_format
        env.filters["month_to_russian_title"] = month_to_russian_title
        return env

    def _init_watchdoc_folder(self):
        folder = self.ds.obtain_folder(name=WATCHDOC_FOLDER)
        log.info(f"`{WATCHDOC_FOLDER}` web view link: "
                 f"{folder['webViewLink']}")
        return folder

    def _init_applicants_folder(self):
        folder = self.ds.obtain_folder(
            name=APPLICANTS_FOLDER,
            parents=[self._watchdoc_folder["id"]],
        )
        log.info(f"`{APPLICANTS_FOLDER}` web view link: "
                 f"{folder['webViewLink']}")
        return folder

    def _init_campuses_folder(self):
        folder = self.ds.obtain_folder(
            name=CAMPUSES_FOLDER,
            parents=[self._applicants_folder["id"]],
        )
        log.info(f"`{CAMPUSES_FOLDER}` web view link: "
                 f"{folder['webViewLink']}")
        return folder

    def _init_campus_folders(self):
        folders = {}
        for abbr, campus in Campus.choices():
            folders[abbr] = self.ds.obtain_folder(
                name=campus,
                parents=[self._campuses_folder["id"]],
            )
        return folders
