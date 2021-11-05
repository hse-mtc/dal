from django.core.files.base import ContentFile

from common.utils.populate import get_or_create

from dms.models.documents import File


def create_files() -> list[File]:
    files = []

    for i in range(25):
        name = f"document_id_{i}.txt",
        fields = dict(
            name=name,
            content=ContentFile("some content here", name=name),
        )
        file = get_or_create(File, **fields)
        files.append(file)

    return files
