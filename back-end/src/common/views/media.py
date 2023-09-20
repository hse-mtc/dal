import os
import posixpath
from pathlib import Path

from django.http import FileResponse, HttpResponseNotFound
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from dms.models.documents import File


class StaticMediaView(APIView):
    permission_classes = [AllowAny]
    media_root = ""

    def __init__(self, media_root: Path = "/", *args, **kwargs):
        self.media_root = media_root
        super().__init__(*args, **kwargs)

    def get(self, request, request_path, *args, **kwargs):
        request_path = posixpath.normpath(request_path).lstrip("/")
        filename = self.media_root / request_path
        if os.path.exists(filename):
            basename = os.path.basename(filename)
            file_object = File.objects.filter(id=basename)
            if not file_object.exists():
                name = ""
            else:
                name = file_object.get().name
            response = FileResponse(open(filename, "rb"), filename=name)
            return response
        else:
            return HttpResponseNotFound("<h1>Page not found</h1>")
