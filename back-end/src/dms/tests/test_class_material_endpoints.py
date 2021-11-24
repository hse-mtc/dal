import json

import pytest
from django.test.client import MULTIPART_CONTENT, BOUNDARY, encode_multipart
from dms.models.class_materials import ClassMaterial
from dms.models.documents import File


def assert_files_equal(file_data, file_data_original):
    file = File.objects.get(id=file_data["content"].rsplit("/", maxsplit=1)
                            [-1].rsplit("_", maxsplit=1)[0])

    assert file.name == file_data_original["name"]
    assert file.content.open("r").read() == \
           file_data_original["content"].open("r").read()


def assert_class_materials_equal(data, data_original):
    compared_fields = data.keys() - ["file"]

    assert_files_equal(data["file"], data_original["file"])
    assert {field_name: data[field_name] for field_name in compared_fields} == {
        field_name: data_original[field_name] for field_name in compared_fields
    }


def assert_class_material_equal_to_id(su_client, original_data, material_id):
    get_response = su_client.get(f"/api/dms/class-materials/{material_id}/")
    assert get_response.status_code == 200

    response_data = get_response.data
    assert_class_materials_equal(data=response_data,
                                 data_original=original_data)


def multipart_cl_material_data(data):
    multipart_data = data.copy()
    multipart_data["data"] = json.dumps(multipart_data["data"])
    return multipart_data


@pytest.mark.django_db
def test_get_class_materials(su_client, create_class_materials,
                             get_class_material_data):
    count = 3
    data = []
    for _ in range(count):
        c_m = create_class_materials()
        cm_data = get_class_material_data(c_m.topic.id)
        cm_data["id"] = c_m.id
        data.append(cm_data)

    response = su_client.get("/api/dms/class-materials/")
    assert response.status_code == 200
    for data_ in data:
        assert_class_material_equal_to_id(su_client=su_client,
                                          material_id=data_["id"],
                                          original_data=data_)
    assert len(response.data) == count


@pytest.mark.django_db
def test_class_materials_delete(su_client, create_class_materials):
    material = create_class_materials()

    assert len(ClassMaterial.objects.all()) == 1
    responce = su_client.delete(f"/api/dms/class-materials/{material.id}/")
    assert responce.status_code == 204
    assert len(ClassMaterial.objects.all()) == 0


@pytest.mark.django_db
def test_class_materials_post(su_client, create_topic, get_class_material_data):
    topic = create_topic
    data = get_class_material_data(topic_id=topic.id)

    patch_fields = ["title", "annotation", "upload_date", "type", "topic"]

    patch_data = {
        "data": {field_name: data[field_name] for field_name in patch_fields},
        "content": data["file"]["content"]
    }

    response = su_client.post("/api/dms/class-materials/",
                              data=multipart_cl_material_data(patch_data))
    data["id"] = response.data["id"]
    assert response.status_code == 201

    assert_class_material_equal_to_id(su_client=su_client,
                                      original_data=data,
                                      material_id=data["id"])


@pytest.mark.django_db
def test_class_materials_put(su_client, create_class_materials,
                             get_class_material_data, get_file_model_data):
    material = create_class_materials()

    data = get_class_material_data(topic_id=material.topic.id)
    data["id"] = material.id
    data["title"] = "New title"
    data["upload_date"] = "2021-11-17"
    data["annotation"] = "New annotation"
    data["type"] = ClassMaterial.Type.SEMINARS.value

    put_fields = ["title", "annotation", "upload_date", "type", "topic"]

    data["file"] = get_file_model_data(raw_file_body="Matter of Trust",
                                       file_name="Billy.txt")
    file = data["file"]["content"]

    put_data = {
        "data": {field_name: data[field_name] for field_name in put_fields},
        "content": file
    }

    content = encode_multipart(boundary=BOUNDARY,
                               data=multipart_cl_material_data(put_data))

    response = su_client.put(f"/api/dms/class-materials/{material.id}/",
                             data=content,
                             content_type=MULTIPART_CONTENT)
    assert response.status_code == 200

    assert_class_material_equal_to_id(su_client=su_client,
                                      original_data=data,
                                      material_id=material.id)


@pytest.mark.django_db
def test_class_materials_patch(su_client, create_class_materials,
                               get_class_material_data, get_file_model_data):
    material = create_class_materials()

    data = get_class_material_data(topic_id=material.topic.id)
    data["id"] = material.id
    data["title"] = "New title"
    data["upload_date"] = "2021-11-17"
    data["annotation"] = "New annotation"
    data["type"] = ClassMaterial.Type.SEMINARS.value

    patch_fields = ["title", "annotation", "upload_date", "type"]

    data["file"] = get_file_model_data(raw_file_body="Matter of Trust",
                                       file_name="Billy.txt")
    file = data["file"]["content"]

    patch_data = {
        "data": {field_name: data[field_name] for field_name in patch_fields},
        "content": file
    }

    content = encode_multipart(boundary=BOUNDARY,
                               data=multipart_cl_material_data(patch_data))

    response = su_client.patch(f"/api/dms/class-materials/{material.id}/",
                               data=content,
                               content_type=MULTIPART_CONTENT)
    assert response.status_code == 200

    assert_class_material_equal_to_id(su_client=su_client,
                                      original_data=data,
                                      material_id=material.id)
