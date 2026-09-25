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

OFFICE_EXTENSIONS = {
    "doc",
    "docx",
    "odp",
    "ods",
    "odt",
    "ppt",
    "pptx",
    "rtf",
    "xls",
    "xlsx",
}


class PreviewConversionError(Exception):
    """Raised when an office document cannot be converted for preview."""


def get_extension(filename: str) -> str:
    return Path(filename or "").suffix.lstrip(".").lower()


def get_preview_kind(filename: str):
    extension = get_extension(filename)
    if extension in OFFICE_EXTENSIONS:
        return "document"
    return NATIVE_PREVIEW_KINDS.get(extension)


def requires_conversion(filename: str) -> bool:
    return get_extension(filename) in OFFICE_EXTENSIONS


def preview_cache_path(media_root: Path, file_id) -> Path:
    return Path(media_root) / "previews" / f"{file_id}.pdf"


def remove_cached_preview(media_root: Path, file_id):
    preview_path = preview_cache_path(media_root, file_id)
    try:
        preview_path.unlink()
    except FileNotFoundError:
        pass


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
