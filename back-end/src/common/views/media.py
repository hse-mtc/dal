import logging
import mimetypes
import os
import posixpath
from pathlib import Path

from django.core.exceptions import ValidationError
from django.http import (
    FileResponse,
    HttpResponse,
    HttpResponseNotFound,
    JsonResponse,
)
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from dms.models.documents import File
from dms.previews import (
    PreviewConversionError,
    get_or_create_pdf_preview,
    get_preview_kind,
    requires_conversion,
)


logger = logging.getLogger(__name__)


class StaticMediaView(APIView):
    permission_classes = [AllowAny]
    media_root = ""

    def __init__(self, media_root: Path = "/", *args, **kwargs):
        self.media_root = media_root
        super().__init__(*args, **kwargs)

    def get(self, request, request_path, *args, **kwargs):
        request_path = posixpath.normpath(request_path).lstrip("/")
        media_root = Path(self.media_root).resolve()
        filename = (media_root / request_path).resolve()
        is_preview = request.query_params.get("preview") == "1"

        try:
            filename.relative_to(media_root)
        except ValueError:
            return HttpResponseNotFound("<h1>Page not found</h1>")

        if filename.is_file():
            basename = os.path.basename(filename)
            try:
                file_object = File.objects.filter(id=basename).first()
            except (ValidationError, ValueError):
                file_object = None
            name = file_object.name if file_object else basename

            if is_preview:
                if file_object is None or not get_preview_kind(name):
                    return JsonResponse(
                        {"detail": "Preview is not available for this file."},
                        status=415,
                    )

                if requires_conversion(name):
                    try:
                        filename = get_or_create_pdf_preview(
                            source_path=filename,
                            original_name=name,
                            media_root=self.media_root,
                            file_id=basename,
                        )
                    except PreviewConversionError as error:
                        logger.warning("Could not prepare file preview: %s", error)
                        return JsonResponse(
                            {"detail": "Could not prepare the file preview."},
                            status=503,
                        )
                    name = f"{Path(name).stem}.pdf"

            content_type = mimetypes.guess_type(name)[0] or "application/octet-stream"

            file_size = os.path.getsize(filename)
            range_header = request.headers.get("Range")

            if range_header:
                start, end = self.parse_range_header(range_header, file_size)
                if start is not None and end is not None:
                    with open(filename, "rb") as file_handle:
                        file_handle.seek(start)
                        response = HttpResponse(
                            file_handle.read(end - start + 1),
                            status=206,
                            content_type=content_type,
                        )
                    response["Content-Range"] = f"bytes {start}-{end}/{file_size}"
                    response["Content-Length"] = str(end - start + 1)
                    response["Content-Disposition"] = f'inline; filename="{name}"'
                    response["Accept-Ranges"] = "bytes"
                    if is_preview:
                        response["X-Frame-Options"] = "SAMEORIGIN"
                    return response

            response = FileResponse(
                open(filename, "rb"),
                filename=name,
                as_attachment=False,
                content_type=content_type,
            )
            response["Accept-Ranges"] = "bytes"
            if is_preview:
                response["X-Frame-Options"] = "SAMEORIGIN"
            return response
        else:
            return HttpResponseNotFound("<h1>Page not found</h1>")

    @staticmethod
    def parse_range_header(range_header: str, file_size: int):
        if not range_header.startswith("bytes="):
            return None, None

        ranges = range_header.replace("bytes=", "", 1).split("-", 1)
        if len(ranges) != 2:
            return None, None

        start_str, end_str = ranges
        if not start_str and not end_str:
            return None, None

        if not start_str:
            length = int(end_str)
            return max(file_size - length, 0), file_size - 1

        start = int(start_str)
        end = int(end_str) if end_str else file_size - 1

        if start >= file_size:
            return None, None

        return start, min(end, file_size - 1)
