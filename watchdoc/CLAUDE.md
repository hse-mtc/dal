# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Purpose

Stateless FastAPI service that generates DOCX documents for applicants, uploads them to Yandex Disk, and sends an email notification with a shared folder link.

## Endpoints (`src/main.py`)

| Method | Path                | Description                                                        |
|--------|---------------------|--------------------------------------------------------------------|
| POST   | `/applicants/`      | Generate all applicant documents, upload to Yandex Disk, send email (background task) |
| GET    | `/generate_docs/`   | Generate only the "Анкета абитуриента" form for a list of applicants, return as ZIP |

Both endpoints accept an `Applicant` (or list) Pydantic model defined in `src/proto.py`.

## Document Generation

Templates are DOCX files in `templates/` rendered with `docxtpl` (Jinja2 for Word). Template-to-output name mapping is defined in `src/main.py`.

Two custom Jinja2 filters are registered:
- `date_to_russian_format` — converts a date to `DD.MM.YYYY`
- `month_to_russian_title` — converts month number to Russian month name (genitive)

The `Applicant` model contains `photo` as a Base64-encoded string. During rendering this is decoded and embedded inline in the document.

## Yandex Disk Integration (`src/disk.py`)

Folder structure on disk:
```
watchdoc/Абитуриенты/Кампусы/{campus_name}/{applicant_surname} {applicant_name} {email}/
```

Key operations: create folder if missing (`obtain_folder`), upload DOCX files, make the folder publicly shareable and return the link.

## Email (`src/email_service.py`)

SMTP with TLS. Sends an HTML email to the applicant's corporate email after upload. The email contains the Yandex Disk shared link and instructions.

## Adding a New Document

1. Add a DOCX template to `templates/`
2. Add the template filename → output filename mapping in `main.py`
3. Extend the Jinja2 context dict in the generation function with any new fields from `Applicant`

## Configuration (`src/config.py`)

Key env vars: `YADISK_TOKEN`, SMTP settings (`EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_USER`, `EMAIL_PASSWORD`, `EMAIL_USE_TLS`), `WATCHDOC_PORT`, `DEBUG`.
