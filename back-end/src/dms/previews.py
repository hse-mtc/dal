import os
import shutil
import subprocess
import tempfile
from pathlib import Path


NATIVE_PREVIEW_KINDS = {
    "pdf": "document",
    "bmp": "image",
    "gif": "image",
    "jpeg": "image",
    "jpg": "image",
    "png": "image",
    "svg": "image",
    "webp": "image",
    "aac": "audio",
    "flac": "audio",
    "m4a": "audio",
    "mp3": "audio",
    "oga": "audio",
    "ogg": "audio",
    "wav": "audio",
    "m4v": "video",
    "mov": "video",
    "mp4": "video",
    "ogv": "video",
    "webm": "video",
    "csv": "text",
    "json": "text",
    "log": "text",
    "md": "text",
    "txt": "text",
    "xml": "text",
}

PRESENTATION_EXTENSIONS = {
    "odp",
    "ppt",
    "pptx",
}

OFFICE_EXTENSIONS = {
    "doc",
    "docx",
    "ods",
    "odt",
    "rtf",
    "xls",
    "xlsx",
} | PRESENTATION_EXTENSIONS


class PreviewConversionError(Exception):
    """Raised when an office document cannot be converted for preview."""


class PreviewPageError(Exception):
    """Raised when a requested presentation page does not exist."""


def get_extension(filename: str) -> str:
    return Path(filename or "").suffix.lstrip(".").lower()


def get_preview_kind(filename: str):
    extension = get_extension(filename)
    if extension in PRESENTATION_EXTENSIONS:
        return "presentation"
    if extension in OFFICE_EXTENSIONS:
        return "document"
    return NATIVE_PREVIEW_KINDS.get(extension)


def requires_conversion(filename: str) -> bool:
    return get_extension(filename) in OFFICE_EXTENSIONS


def preview_cache_path(media_root: Path, file_id) -> Path:
    return Path(media_root) / "previews" / f"{file_id}.pdf"


def slide_cache_path(media_root: Path, file_id, page_number: int) -> Path:
    return Path(media_root) / "previews" / str(file_id) / f"slide-{page_number}.png"


def remove_cached_preview(media_root: Path, file_id):
    preview_path = preview_cache_path(media_root, file_id)
    try:
        preview_path.unlink()
    except FileNotFoundError:
        pass
    shutil.rmtree(preview_path.with_suffix(""), ignore_errors=True)


def get_pdf_page_count(pdf_path: Path) -> int:
    executable = shutil.which("pdfinfo")
    if executable is None:
        raise PreviewConversionError("pdfinfo is not installed")

    try:
        result = subprocess.run(
            [executable, str(pdf_path)],
            check=False,
            capture_output=True,
            text=True,
            timeout=15,
            env={**os.environ, "LC_ALL": "C"},
        )
    except (OSError, subprocess.TimeoutExpired) as error:
        raise PreviewConversionError(str(error)) from error

    if result.returncode != 0:
        details = result.stderr.strip() or result.stdout.strip()
        raise PreviewConversionError(details or "Could not read PDF metadata")

    for line in result.stdout.splitlines():
        key, separator, value = line.partition(":")
        if separator and key.strip() == "Pages":
            try:
                return int(value.strip())
            except ValueError as error:
                raise PreviewConversionError("Invalid PDF page count") from error

    raise PreviewConversionError("PDF page count is missing")


def get_or_create_slide_preview(
    pdf_path: Path,
    media_root: Path,
    file_id,
    page_number: int,
) -> tuple[Path, int]:
    pdf_path = Path(pdf_path)
    page_count = get_pdf_page_count(pdf_path)
    if page_number < 1 or page_number > page_count:
        raise PreviewPageError(
            f"Page {page_number} is outside the range 1-{page_count}"
        )

    slide_path = slide_cache_path(media_root, file_id, page_number)
    if slide_path.exists() and slide_path.stat().st_mtime >= pdf_path.stat().st_mtime:
        return slide_path, page_count

    executable = shutil.which("pdftoppm")
    if executable is None:
        raise PreviewConversionError("pdftoppm is not installed")

    slide_path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="dal-slide-") as workdir:
        output_prefix = Path(workdir) / "slide"
        command = [
            executable,
            "-f",
            str(page_number),
            "-l",
            str(page_number),
            "-singlefile",
            "-png",
            "-scale-to-x",
            "1920",
            "-scale-to-y",
            "-1",
            str(pdf_path),
            str(output_prefix),
        ]

        try:
            result = subprocess.run(
                command,
                check=False,
                capture_output=True,
                text=True,
                timeout=60,
            )
        except (OSError, subprocess.TimeoutExpired) as error:
            raise PreviewConversionError(str(error)) from error

        rendered_path = output_prefix.with_suffix(".png")
        if result.returncode != 0 or not rendered_path.exists():
            details = result.stderr.strip() or result.stdout.strip()
            raise PreviewConversionError(details or "Slide rendering failed")

        temporary_slide_path = slide_path.with_suffix(f".{os.getpid()}.tmp")
        shutil.copyfile(rendered_path, temporary_slide_path)
        os.replace(temporary_slide_path, slide_path)

    return slide_path, page_count


def get_or_create_pdf_preview(
    source_path: Path,
    original_name: str,
    media_root: Path,
    file_id,
) -> Path:
    source_path = Path(source_path)
    preview_path = preview_cache_path(media_root, file_id)

    if (
        preview_path.exists()
        and preview_path.stat().st_mtime >= source_path.stat().st_mtime
    ):
        return preview_path

    executable = shutil.which("libreoffice") or shutil.which("soffice")
    if executable is None:
        raise PreviewConversionError("LibreOffice is not installed")

    extension = get_extension(original_name)
    preview_path.parent.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory(prefix="dal-preview-") as workdir:
        workdir_path = Path(workdir)
        input_path = workdir_path / f"source.{extension}"
        output_dir = workdir_path / "output"
        profile_dir = workdir_path / "profile"
        output_dir.mkdir()
        profile_dir.mkdir()
        shutil.copyfile(source_path, input_path)

        command = [
            executable,
            f"-env:UserInstallation={profile_dir.as_uri()}",
            "--headless",
            "--nologo",
            "--nodefault",
            "--nolockcheck",
            "--nofirststartwizard",
            "--convert-to",
            "pdf",
            "--outdir",
            str(output_dir),
            str(input_path),
        ]

        try:
            result = subprocess.run(
                command,
                check=False,
                capture_output=True,
                text=True,
                timeout=60,
            )
        except (OSError, subprocess.TimeoutExpired) as error:
            raise PreviewConversionError(str(error)) from error

        converted_path = output_dir / "source.pdf"
        if result.returncode != 0 or not converted_path.exists():
            details = result.stderr.strip() or result.stdout.strip()
            raise PreviewConversionError(details or "Document conversion failed")

        temporary_preview_path = preview_path.with_suffix(f".{os.getpid()}.tmp")
        shutil.copyfile(converted_path, temporary_preview_path)
        os.replace(temporary_preview_path, preview_path)

    return preview_path
