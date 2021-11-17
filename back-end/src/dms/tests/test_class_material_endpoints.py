from dms.models.class_materials import ClassMaterial


def test_class_materials_delete(su_client, create_class_materials):
    material = create_class_materials

    assert len(ClassMaterial.objects.all()) == 1
    su_client.delete(f'/api/dms/class-materials/{material.id}/')
    assert len(ClassMaterial.objects.all()) == 0


def test_class_materials_patch(su_client, create_class_materials, get_class_material_data):
    material = create_class_materials

    assert material.type == ClassMaterial.Type.LECTURES.value

    print(su_client.get(f'/api/dms/class-materials/{material.id}/').data)
    print(material.topic.id)
    data = get_class_material_data(type_=ClassMaterial.Type.SEMINARS.value, topic_id=material.topic.id)
    print(data)
    data['id'] = material.id
    su_client.patch(f'/api/dms/class-materials/{material.id}/', data=data)
    #assert material.type == ClassMaterial.Type.SEMINARS.value