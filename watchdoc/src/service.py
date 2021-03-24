import logging as log

import jinja2

from docxtpl import DocxTemplate

from drive import DriveService
from campuses import Campus
from proto import Applicant
from config import (
    TEMPLATES_DIR,
    GENERATED_DIR,
)
from date_utils import (
    date_to_russian_format,
    month_to_russian_title,
    today,
)

WATCHDOC_FOLDER: str = "watchdoc"
APPLICANTS_FOLDER: str = "Абитуриенты"
CAMPUSES_FOLDER: str = "Кампусы"


class WatchDocService:
    def __init__(self) -> None:
        self.ds = DriveService()

        # watchdoc folder

        self._watchdoc_folder = self.ds.obtain_folder(name=WATCHDOC_FOLDER, )
        self.ds.write_share_folder_with_admin(
            folder_id=self._watchdoc_folder["id"], )
        log.info(f"`{WATCHDOC_FOLDER}` web view link: "
                 f"{self._watchdoc_folder['webViewLink']}")

        # applicants folder

        self._applicants_folder = self.ds.obtain_folder(
            name=APPLICANTS_FOLDER,
            parents=[self._watchdoc_folder["id"]],
        )
        log.info(f"`{APPLICANTS_FOLDER}` web view link: "
                 f"{self._applicants_folder['webViewLink']}")

        # campus folders

        self._campuses_folder = self.ds.obtain_folder(
            name=CAMPUSES_FOLDER,
            parents=[self._applicants_folder["id"]],
        )
        log.info(f"`{CAMPUSES_FOLDER}` web view link: "
                 f"{self._campuses_folder['webViewLink']}")

        self._campus_folders = {}
        for abbr, campus in Campus.choices():
            self._campus_folders[abbr] = self.ds.obtain_folder(
                name=campus,
                parents=[self._campuses_folder["id"]],
            )

    def generate_documents(self, applicant: Applicant):
        template_path = TEMPLATES_DIR / "mec-application.docx"
        doc = DocxTemplate(template_path)

        jinja_env = jinja2.Environment()
        jinja_env.filters["date_to_russian_format"] = date_to_russian_format
        jinja_env.filters["month_to_russian_title"] = month_to_russian_title

        context = {
            "date": today(),
            **applicant.dict(),
        }
        doc.render(context, jinja_env)

        applicant_dir = GENERATED_DIR / applicant.contact_info.corporate_email
        applicant_dir.mkdir(exist_ok=True)
        generated_path = applicant_dir / "mec-application.docx"
        doc.save(generated_path)
