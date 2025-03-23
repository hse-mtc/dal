from import_export import resources
from rest_framework import serializers
from common.models.recruitment_office import RecruitmentOffice

class RecruitmentOfficeSerializer(serializers.ModelSerializer):
    display = serializers.SerializerMethodField()

    class Meta:
        model = RecruitmentOffice
        fields = ['city', 'name', 'display']

    def get_display(self, obj):
        return f"{obj.city} - {obj.name}"


class RecruitmentOfficeResource(resources.ModelResource):
    class Meta:
        model = RecruitmentOffice
        import_id_fields = ()
        fields = ('city', 'name')
