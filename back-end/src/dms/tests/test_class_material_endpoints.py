import json

from django.core.files.base import ContentFile
from django.test.client import MULTIPART_CONTENT, BOUNDARY, encode_multipart
from dms.models.class_materials import ClassMaterial
from dms.models.documents import File


def assert_files_equal(file_data, file_data_original):
    file = File.objects.get(id=file_data["content"].rsplit(
        "/", maxsplit=1)[-1].rsplit("_", maxsplit=1)[0])

    assert file.name == file_data_original["name"]
    assert file.content.open("r").read() == \
           file_data_original["content"].open("r").read()


def assert_class_materials_equal(su_client, data, material_id):
    get_response = su_client.get(f'/api/dms/class-materials/{material_id}/')
    assert get_response.status_code == 200

    response_data = get_response.data

    compared_fields = response_data.keys() - ["file"]

    assert_files_equal(response_data["file"], data["file"])
    assert {
               field_name: response_data[field_name]
               for field_name in compared_fields
           } == {
               field_name: data[field_name]
               for field_name in compared_fields
           }


def test_get_class_materials(su_client, create_class_materials, get_class_material_data):
    count = 3
    data = []
    for i in range(count):
        cm = create_class_materials()
        cm_data = get_class_material_data(cm.topic.id)
        cm_data["id"] = cm.id
        data.append(cm_data)

    response = su_client.get("/api/dms/class-materials/")
    assert response.status_code == 200
    for data_ in data:
        assert_class_materials_equal(su_client=su_client, material_id=data_["id"], data=data_)
    assert len(response.data) == count


def test_class_materials_delete(su_client, create_class_materials):
    material = create_class_materials()

    assert len(ClassMaterial.objects.all()) == 1
    responce = su_client.delete(f'/api/dms/class-materials/{material.id}/')
    assert responce.status_code == 204
    assert len(ClassMaterial.objects.all()) == 0


def test_class_materials_patch(su_client, create_class_materials, get_class_material_data):
    material = create_class_materials()

    data = get_class_material_data(topic_id=material.topic.id)
    data["id"] = material.id
    data["title"] = "New title"
    data["upload_date"] = "2021-11-17"
    data["annotation"] = "New annotation"
    data["type"] = ClassMaterial.Type.SEMINARS.value

    patch_fields = [
        "title", "annotation", "upload_date", "type"
    ]

    patch_data = {
        field_name: data[field_name]
        for field_name in patch_fields
    }

    file = ContentFile("file_content_new_2", name="file.txt")

    content = encode_multipart(
        boundary=BOUNDARY,
        data={
            "contenet": file,
            "data": json.dumps(patch_data)
        }
    )

    responce = su_client.patch(f'/api/dms/class-materials/{material.id}/', data=content,
                               content_type=MULTIPART_CONTENT)
    assert responce.status_code == 200

    assert_class_materials_equal(su_client=su_client, data=data, material_id=material.id)

