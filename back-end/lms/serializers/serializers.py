from rest_framework.serializers import (ModelSerializer, IntegerField, 
                                        CharField)

from lms.models import (
    Milgroup,
    Program,
)


class NestedModelSerializer(ModelSerializer):
    nested_fields = []

    def create(self, validated_data):
        nested_data = {}
        for field_data in self.nested_fields:
            # for fields like milgroup, which are a dict themselves
            if len(field_data) == 2:
                field, model = field_data
                nested_data[field] = model.objects.get(**validated_data.pop(field))
            # for fields like rank, which is just a field. Therefore a param for model
            # has to be specified
            else:
                field, model, param = field_data
                nested_data[field] = model.objects.get(**{
                    param: validated_data.pop(field)})
        return self.Meta.model.objects.create(**nested_data, **validated_data)
    
    def update(self, instance, validated_data):
        for field_data in self.nested_fields:
            if field_data[0] in validated_data:
                # for fields like milgroup, which are a dict themselves
                if len(field_data) == 2:
                    field, model = field_data
                    new_data = model.objects.get(**validated_data.pop(field))
                # for fields like rank, which is just a field. Therefore a param for model
                # has to be specified
                else:
                    field, model, param = field_data
                    new_data = model.objects.get(**{
                        param: validated_data.pop(field)})
                # set instance attribute
                setattr(instance, field, new_data)
        
        # set attributes for other keys in validated data
        for k, v in validated_data.items():
            setattr(instance, k, v)
        instance.save()

        return instance


class MilgroupSerializer(ModelSerializer):
    milgroup = IntegerField()
    milfaculty = CharField(required=False)

    class Meta:
        model = Milgroup
        fields = '__all__'


class ProgramSerializer(ModelSerializer):

    class Meta:
        model = Program
        fields = '__all__'
        extra_kwargs = {'code': {'validators': []}}
