import logging as log

import jinja2

from docxtpl import DocxTemplate

from auth import obtain_credentials
from gmail import GmailService
from drive import DriveService
from campuses import Campus
from proto import Applicant
from config import (
    TEMPLATES_DIR,
    GENERATED_DIR,
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

DOCUMENTS = [
    ("mec-application.docx", "Заявление на поступление.docx"),
    ("ro-reference.docx", "Направление ВК.docx"),
]


class WatchDocService:
    """WatchDoc manages applicants' documents.

    Usage:
        wds = WatchDocService()
        wds.generate_documents(applicant)
        folder_link = wds.upload_documents(applicant)
        wds.notify(applicant, folder_link)
    """
    def generate_documents(self, applicant: Applicant):
        applicant_dir = GENERATED_DIR / applicant.contact_info.corporate_email
        applicant_dir.mkdir(exist_ok=True)

        context = {
            "date": today(),
            **applicant.dict(),
        }

        for (en, rus) in DOCUMENTS:
            doc = DocxTemplate(TEMPLATES_DIR / en)
            doc.render(context, self.jinja_env)
            doc.save(applicant_dir / rus)

    def upload_documents(self, applicant: Applicant):
        email = applicant.contact_info.corporate_email
        campus = applicant.university_info.campus.value
        folder_name = f"{applicant.full_name} {email}"

        applicant_folder = self.ds.obtain_folder(
            name=folder_name,
            parents=[self._campus_folders[campus]["id"]],
        )
        documents_folder = self.ds.obtain_folder(
            name="Документы",
            parents=[applicant_folder["id"]],
        )

        for (_, rus) in DOCUMENTS:
            body = {
                "name": rus,
                "parents": [documents_folder["id"]],
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
        self.gs.send_message(body=msg)

    # --------------------------------------------------------------------------
    # Internal methods

    def __init__(self) -> None:
        # Templates
        self.jinja_env = self._init_jinja_env()

        # Credentials
        credentials = obtain_credentials()

        # Gmail
        self.gs = GmailService(credentials)

        # Drive
        self.ds = DriveService(credentials)
        self._watchdoc_folder = self._init_watchdoc_folder()
        self._applicants_folder = self._init_applicants_folder()
        self._campuses_folder = self._init_campuses_folder()
        self._campus_folders = self._init_campus_folders()

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
