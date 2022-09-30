import logging as log
import os
import zipfile

from fastapi import (
    FastAPI,
    Response,
    BackgroundTasks,
)

from service import WatchDocService
from proto import Applicant
from config import (
    TEMP_DIR,
    WATCHDOC_PORT,
    DEBUG, GENERATED_DIR,
)

from typing import List

from fastapi.responses import FileResponse

log.basicConfig(
    level="INFO",
    format="[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s",
)

watchdoc = FastAPI()
wds = WatchDocService()


@watchdoc.post("/applicants/")
def post_applicant(applicant: Applicant, background_tasks: BackgroundTasks):
    def closure():
        email = applicant.contact_info.corporate_email

        log.info(f"{email}: generating documents...")
        wds.generate_documents(applicant)

        log.info(f"{email}: uploading documents...")
        folder_link = wds.upload_documents(applicant)

        log.info(f"{email}: notifying applicant...")
        wds.notify(applicant, folder_link)

    background_tasks.add_task(closure)
    return "Templates are being generated, wait for the link"


@watchdoc.get("/generate_docs/")
def get_docs(applicants: list[Applicant], background_tasks: BackgroundTasks):
    for applicant in applicants:
        email = applicant.contact_info.corporate_email

        log.info(f"{email}: generating documents...")
        wds.generate_documents(applicant, 
            docs=[("applicant-form.docx", "Анкета абитуриента.docx")])

    docs_zip = zipfile.ZipFile(TEMP_DIR / "docs.zip", "w")

    for folder, subfolders, files in os.walk(GENERATED_DIR):
        for file in files:
            if file in ["Анкета абитуриента.docx"]:
                docs_zip.write(os.path.join(folder, file),
                                os.path.relpath(os.path.join(folder, file), GENERATED_DIR),
                                compress_type=zipfile.ZIP_DEFLATED)

    docs_zip.close()

    with open(TEMP_DIR / "docs.zip", 'rb') as file_data:
        bytes_content = file_data.read()
    return Response(content=bytes_content, media_type="application/zip")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:watchdoc",
        host="0.0.0.0",
        port=WATCHDOC_PORT,
        debug=DEBUG,
    )
