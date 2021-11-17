from src.dms.models.class_materials import ClassMaterial


def test_class_materials_delete(su_client, create_class_materials):
    material = create_class_materials

    assert len(ClassMaterial.objects.all()) == 1
    su_client.delete(f'/api/dms/class-materials/{material.id}/')
    assert len(ClassMaterial.objects.all()) == 0


