import os
import subprocess
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import mock

from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APIRequestFactory

from common.views.media import StaticMediaView
from dms.models.documents import File
from dms.previews import (
    get_or_create_pdf_preview,
    get_or_create_slide_preview,
    get_preview_kind,
    requires_conversion,
)


def test_preview_kinds():
    assert get_preview_kind("document.PDF") == "document"
    assert get_preview_kind("lecture.docx") == "document"
    assert get_preview_kind("slides.PPTX") == "presentation"
    assert get_preview_kind("slides.odp") == "presentation"
    assert get_preview_kind("photo.jpeg") == "image"
    assert get_preview_kind("recording.mp3") == "audio"
    assert get_preview_kind("lesson.webm") == "video"
    assert get_preview_kind("notes.txt") == "text"
    assert get_preview_kind("archive.zip") is None


def test_office_files_require_conversion():
    assert requires_conversion("document.docx")
    assert requires_conversion("table.xlsx")
    assert not requires_conversion("document.pdf")


def test_pdf_preview_is_created_and_cached():
    with TemporaryDirectory() as directory:
        root = Path(directory)
        media_root = root / "media"
        source = root / "source"
        source.write_bytes(b"office document")

        def fake_run(command, **kwargs):
            output_dir = Path(command[command.index("--outdir") + 1])
            (output_dir / "source.pdf").write_bytes(b"pdf preview")
            return subprocess.CompletedProcess(command, 0, "", "")

        with mock.patch("dms.previews.shutil.which", return_value="libreoffice"):
            with mock.patch("dms.previews.subprocess.run", side_effect=fake_run) as run:
                preview = get_or_create_pdf_preview(
                    source_path=source,
                    original_name="lecture.docx",
                    media_root=media_root,
                    file_id="file-id",
                )

                assert preview.read_bytes() == b"pdf preview"
                assert run.call_count == 1

                os.utime(preview, (source.stat().st_mtime + 1,) * 2)
                cached_preview = get_or_create_pdf_preview(
                    source_path=source,
                    original_name="lecture.docx",
                    media_root=media_root,
                    file_id="file-id",
                )

                assert cached_preview == preview
                assert run.call_count == 1


def test_presentation_slide_is_rendered_and_cached():
    with TemporaryDirectory() as directory:
        root = Path(directory)
        media_root = root / "media"
        preview = root / "preview.pdf"
        preview.write_bytes(b"pdf preview")

        def fake_run(command, **kwargs):
            if command[0] == "pdfinfo":
                return subprocess.CompletedProcess(
                    command,
                    0,
                    "Pages:          3\n",
                    "",
                )

            Path(f"{command[-1]}.png").write_bytes(b"slide preview")
            return subprocess.CompletedProcess(command, 0, "", "")

        with mock.patch("dms.previews.shutil.which", side_effect=lambda name: name):
            with mock.patch("dms.previews.subprocess.run", side_effect=fake_run) as run:
                slide, page_count = get_or_create_slide_preview(
                    pdf_path=preview,
                    media_root=media_root,
                    file_id="file-id",
                    page_number=2,
                )

                assert slide.read_bytes() == b"slide preview"
                assert page_count == 3
                assert run.call_count == 2

                os.utime(slide, (preview.stat().st_mtime + 1,) * 2)
                cached_slide, cached_page_count = get_or_create_slide_preview(
                    pdf_path=preview,
                    media_root=media_root,
                    file_id="file-id",
                    page_number=2,
                )

                assert cached_slide == slide
                assert cached_page_count == 3
                assert run.call_count == 3


def test_preview_response_can_be_embedded_on_same_origin(settings, tmp_path):
    settings.MEDIA_ROOT = tmp_path
    file_object = File.objects.create(
        content=SimpleUploadedFile("notes.txt", b"Preview text"),
        name="notes.txt",
    )
    request = APIRequestFactory().get(
        file_object.content.url,
        {"preview": "1"},
    )

    response = StaticMediaView.as_view(media_root=tmp_path)(
        request,
        request_path=file_object.content.name,
    )

    assert response.status_code == 200
    assert response["Content-Disposition"] == 'inline; filename="notes.txt"'
    assert response["X-Frame-Options"] == "SAMEORIGIN"


def test_presentation_page_response_has_navigation_metadata(settings, tmp_path):
    settings.MEDIA_ROOT = tmp_path
    file_object = File.objects.create(
        content=SimpleUploadedFile("slides.pptx", b"Presentation"),
        name="slides.pptx",
    )
    pdf_preview = tmp_path / "preview.pdf"
    slide_preview = tmp_path / "slide-2.png"
    pdf_preview.write_bytes(b"pdf")
    slide_preview.write_bytes(b"png")
    request = APIRequestFactory().get(
        file_object.content.url,
        {"preview": "1", "page": "2"},
    )

    with mock.patch(
        "common.views.media.get_or_create_pdf_preview",
        return_value=pdf_preview,
    ):
        with mock.patch(
            "common.views.media.get_or_create_slide_preview",
            return_value=(slide_preview, 4),
        ):
            response = StaticMediaView.as_view(media_root=tmp_path)(
                request,
                request_path=file_object.content.name,
            )

    assert response.status_code == 200
    assert response["Content-Type"] == "image/png"
    assert response["X-Preview-Page-Count"] == "4"
    assert response["X-Frame-Options"] == "SAMEORIGIN"
    assert b"".join(response.streaming_content) == b"png"
