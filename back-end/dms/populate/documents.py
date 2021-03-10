from django.core.files.base import ContentFile

from dms.models.documents import File


def create_files() -> list[File]:
    files = []

    for i in range(25):
        name = f"document_id_{i}.txt"
        content = ContentFile("some content here", name=name)
        file = File.objects.create(content=content, name=name)
        file.save()
        files.append(file)

    return files
